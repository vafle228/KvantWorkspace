from django.views.generic import View
from core.mixins import KvantJournalAccessMixin
from django.shortcuts import redirect, HttpResponse


class UserLogOutView(KvantJournalAccessMixin, View):
    def get(self, *args, **kwargs):
        from django.urls import reverse_lazy
        from django.contrib.auth import logout

        logout(self.request)
        return redirect(reverse_lazy('login_page'))


class UserThemeChangeView(KvantJournalAccessMixin, View):
    def post(self, *args, **kwargs):
        from .forms import UserThemeChangeForm
        
        form = UserThemeChangeForm(self.request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return HttpResponse('OK')  # Бесполезный ответ
        return HttpResponse('Error')
