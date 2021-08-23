from LoginApp.models import KvantUser
from django.views.generic import View
from django.shortcuts import redirect, HttpResponse


class KvantJournalAccessMixin(View):
    # Метод делегирования запроса
    def dispatch(self, request, *args, **kwargs):
        from django.urls import reverse_lazy
        
        user_id = kwargs['identifier']
        if not self.is_available(user_id):  # Проверка на доступ
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)  # Исполняем родительский метод

    def is_available(self, identifier):
        from django.contrib import messages

        if KvantUser.objects.filter(id=identifier).exists():  # Проверяем существование
            request_user = self.request.user  # Пользователь который запросил
            requested_user = KvantUser.objects.filter(id=identifier)[0]  # Пользовательн которого запросили
            if request_user == requested_user and requested_user.is_authenticated:  # Проверка совпадения
                return True

        # Ошибка в случаи не совпадения или отсутсвия
        messages.error(self.request, 'Отказано в доступе!')
        return False


class UserLogOutView(KvantJournalAccessMixin, View):
    def post(self, *args, **kwargs):
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
