from LoginApp.models import KvantUser
from .models import TempRegisterLink
from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from django.contrib.auth import login


class RegistrationAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'register_key'
    
    def _objectExiststTest(self, object_id):
        return TempRegisterLink.objects.filter(key=object_id).exists()
    
    def _authenticateTest(self, user): return True


class UserCreatinManager(ObjectManipulationManager):
    def registerUser(self, request, key):
        user_or_errors = self._getCreatedObject(request)

        if isinstance(user_or_errors, KvantUser):
            login(request, user_or_errors); getTempUrlByKey(key).delete()
        return self.getResponse(user_or_errors)

    def _constructRedirectUrl(self, **kwargs): return rl('main_page')


def getUserPersonalInfo(user):
    if hasattr(user, 'studentpersonalinfo'):
        return user.studentpersonalinfo
    return user.staffpersonalinfo


def getTempUrlByKey(key):
    return TempRegisterLink.objects.get(key=key)