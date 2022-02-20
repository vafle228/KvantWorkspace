from django.http import HttpResponse
from django.views import generic
from .forms import UserThemeChangeForm
from .services.access import KvantWorkspaceAccessMixin


class ChangeUserCustomizationView(KvantWorkspaceAccessMixin, generic.View):
    """ Контроллер изменения кастомизации пользователя """
    def post(self, request, *args, **kwargs):
        form = UserThemeChangeForm(
            request.POST, instance=request.user)
        form.save() if form.is_valid() else None
        return HttpResponse({'status': 200})
