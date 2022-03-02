from abc import abstractmethod

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import View


class KvantWorkspaceAccessMixinBase(View):
    """ Рассширение для валидации запросов """
    def dispatch(self, request, *args, **kwargs):
        """ 
        Исполняет все тесты валидации с данными kwargs.
        В случаи завала, возвращает редирект на страницу логина.
        Если был ajax запрос, возвращает JsonResponse
        """
        if not self.accessTest(**kwargs):
            if request.is_ajax():
                return JsonResponse({'status': 'Error', 'message': 'Отказано в доступе!'})
            
            messages.error(self.request, 'Отказано в доступе!')
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)
    
    @abstractmethod
    def accessTest(self, **kwargs):
        """ Собирательный метод для тестов """
        raise NotImplementedError


class KvantWorkspaceAccessMixin(KvantWorkspaceAccessMixinBase):
    """ Рассширение для проверки авторизации """
    def dispatch(self, request, *args, **kwargs):
        kwargs['user'] = request.user
        return super().dispatch(request, *args, **kwargs)
    
    def accessTest(self, **kwargs):
        return self._authenticateTest(kwargs.get('user'))

    def _authenticateTest(self, user):
        """ Тест на авторизованность """
        return user.is_authenticated


class KvantTeacherAndAdminAccessMixin(KvantWorkspaceAccessMixin):
    def accessTest(self, **kwargs):
        user = kwargs.get('user')
        return super().accessTest(**kwargs) and self._permissionTest(user) 

    def _permissionTest(self, user):
        """ Тест на права учителя/администратора """
        return user.permission == 'Учитель' or user.permission == 'Администратор'


class KvantStudentAccessMixin(KvantWorkspaceAccessMixin):
    def accessTest(self, **kwargs):
        user = kwargs.get('user')
        return super().accessTest(**kwargs) and self._permissionTest(user) 

    def _permissionTest(self, user):
        """ Тест на права ученика """
        return user.permission == 'Ученик'


class KvantObjectExistsMixin(KvantWorkspaceAccessMixin):
    request_object_arg = 'object'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'pk_url_kwarg'):
            self.request_object_arg = self.pk_url_kwarg
        return super().dispatch(request, *args, **kwargs)
    
    def accessTest(self, **kwargs):
        object_id = kwargs.get(self.request_object_arg)
        return super().accessTest(**kwargs) and self._objectExiststTest(object_id) 
    
    @abstractmethod
    def _objectExiststTest(self, object_id):
        raise NotImplementedError
