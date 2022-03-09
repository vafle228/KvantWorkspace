from django.shortcuts import redirect
from django.views import generic

from django.contrib.auth import logout
from . import services
from .models import KvantAward
from CoreApp.services.access import KvantWorkspaceAccessMixin
from LoginApp.forms import ImageChangeForm


class SettingsPageTemplateView(KvantWorkspaceAccessMixin, generic.TemplateView):
    template_name = 'ProfileApp/SettingsPage/index.html'


class PortfolioPageListView(KvantWorkspaceAccessMixin, generic.ListView):
    model               = KvantAward
    context_object_name = 'awards'
    template_name       = 'ProfileApp/PortfolioPage/index.html'

    def get_queryset(self):
        return services.getUserAwardsQuery(self.request.user)


class StaticsPageTemplateView(KvantWorkspaceAccessMixin, generic.TemplateView):
    template_name = 'ProfileApp/StatisticsPage/index.html'


class LogoutKvantUserView(KvantWorkspaceAccessMixin, generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login_page')


class KvantUserChangeView(KvantWorkspaceAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.UserChangeManipulationResponse(
            [ImageChangeForm], object=request.user)
        return object_manager.updateObject(request)
        