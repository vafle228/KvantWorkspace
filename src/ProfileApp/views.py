from AdminApp.services import getCourseQuery
from CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import generic
from LoginApp.forms import ImageChangeForm, PasswordChangeForm
from LoginApp.models import KvantUser
from LoginApp.services import getUserById
from ProjectApp.services.services import KvantProjectQuerySelector
from RegisterApp.forms import *

from . import services
from .forms import (KvantAwardSaveForm, SocialInfoBannerSaveForm,
                    SocialInfoSaveForm)


class SettingsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/ProfileInfo/index.html'


class PortfolioPageListView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/ProfilePortfolio/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(awards=services.getUserAwardsQuery(kwargs.get('object')))

        return context


class StaticsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/ProfileStatistics/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(courses=getCourseQuery(kwargs.get('object')))
        
        return context


class ProjectsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/ProfileProjects/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': KvantProjectQuerySelector(
                kwargs.get('object'), {'subject': 'mine'}).getCatalogQuery()
        })
        return context


class LogoutKvantUserView(KvantWorkspaceAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        logout(request); return redirect('login_page')


class KvantUserChangeView(services.UserManipulationMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        self.forms, self.u_func = {
            'image': ([ImageChangeForm], lambda u: u),
            'social': ([SocialInfoSaveForm], lambda u: u.socialinfo),
            'banner': ([SocialInfoBannerSaveForm], lambda u: u.socialinfo),
            'student': ([StudentPersonalInfoSaveForm], lambda u: u.studentpersonalinfo),
            'father': ([StudentParentSaveForm], lambda u: u.studentpersonalinfo.father),
            'mother': ([StudentParentSaveForm], lambda u: u.studentpersonalinfo.mother),
            'staff': ([StaffPersonalInfoSaveForm], lambda u: u.staffpersonalinfo),
        }.get(request.POST.get('type'), (None, None))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = getUserById(self.kwargs.get('user_identifier'))
        object_manager = services.UserManipulationManager(self.forms, object=self.u_func(user))
        return object_manager.updateUserObj(request, user)


class PortfolioAddForm(services.UserExistsMixin, KvantTeacherAndAdminAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(user_identifier=request.POST.get('user'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        object_manager = services.PortfolioManipulationManager([KvantAwardSaveForm])
        return object_manager.createPortfolioInstance(request)


class PasswordChangeView(services.UserManipulationMixin, generic.View):
    def post(self, request, *args, **kwargs):
        user = getUserById(kwargs.get('user_identifier'))
        manager = services.UserChangePasswordManager([PasswordChangeForm], object=user)
        return manager.updateObject(request)
