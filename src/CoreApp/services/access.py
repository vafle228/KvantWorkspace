from abc import abstractmethod

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import View


class KvantWorkspaceAccessMixinBase(View):
    """ Рассширение для валидации запросов """
    def dispatch(self, request, *args, **kwargs):
        """ 
        Исполняет все тесты валидации с данными kwargs.
        В случаи завала, возвращает редирект на страницу логина.
        """
        if not self.accessTest(**kwargs):
            messages.error(self.request, 'Отказано в доступе!')
            return redirect(reverse_lazy('login_page'))
        return super().dispatch(request, *args, **kwargs)
    
    @abstractmethod
    def accessTest(self, **kwargs):
        """ Собирательный метод для тестов """
        raise NotImplementedError


class KvantWorkspaceAccessMixin(KvantWorkspaceAccessMixinBase):
    """ Рассширение для проверки доступа на страницу """
    request_user_arg = 'identifier'

    def dispatch(self, request, *args, **kwargs):
        kwargs['user'] = request.user
        kwargs['requested_id'] = kwargs.get(self.request_user_arg)
        return super().dispatch(request, *args, **kwargs)
    
    def accessTest(self, **kwargs):
        user = kwargs.get('user')
        requested_id = kwargs.get('requested_id')
        return self._authenticateTest(requested_id, user)

    def _authenticateTest(self, requested_id, user):
        """ Тест на авторизованность и совпадения запроса с запрашиваемым """
        return requested_id == user.id and user.is_authenticated


class KvantTeacherAndAdminAccessMixin(KvantWorkspaceAccessMixin):
    def accessTest(self, **kwargs):
        user = kwargs.get('user')
        return self._permissionTest(user) and super().accessTest(**kwargs)

    def _permissionTest(self, user):
        """ Тест на права учителя/администратора """
        return user.permission == 'Учитель' or user.permission == 'Администратор'


class KvantObjectExistsMixin(KvantWorkspaceAccessMixin):
    request_object_arg = 'object'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'pk_url_kwarg'):
            self.request_object_arg = self.pk_url_kwarg
        return super().dispatch(request, *args, **kwargs)
    
    def accessTest(self, **kwargs):
        object_id = kwargs.get(self.request_object_arg)
        return self._objectExiststTest(object_id) and super().accessTest(**kwargs)
    
    @abstractmethod
    def _objectExiststTest(self, object_id):
        raise NotImplementedError
