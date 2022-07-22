from AdminApp.services import getCourseQuery
from CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import generic
from LoginApp.forms import ImageChangeForm
from LoginApp.models import KvantUser
from LoginApp.services import getUserById
from ProjectApp.services.services import KvantProjectQuerySelector

from . import services
from .forms import KvantAwardSaveForm


class SettingsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/SettingsPage/index.html'


class PortfolioPageListView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/PortfolioPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(awards=services.getUserAwardsQuery(kwargs.get('object')))

        return context


class StaticsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/StatisticsPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(courses=getCourseQuery(kwargs.get('object')))
        
        return context


class ProjectsPageTemplateView(services.UserExistsMixin, generic.DetailView):
    model               = KvantUser
    pk_url_kwarg        = 'user_identifier'
    context_object_name = 'requested_user'
    template_name       = 'ProfileApp/ProjectsPage/index.html'

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
    def post(self, request, *args, **kwargs):
        user = getUserById(self.kwargs.get('user_identifier'))
        object_manager = services.UserManipulationManager([ImageChangeForm], object=user)
        return object_manager.updateObject(request)


class PortfolioAddForm(services.UserExistsMixin, KvantTeacherAndAdminAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(user_identifier=request.POST.get('user'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        object_manager = services.PortfolioManipulationManager([KvantAwardSaveForm])
        return object_manager.createPortfolioInstance(request)
        