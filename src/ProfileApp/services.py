from .models import KvantAward
from django.urls import reverse_lazy as rl
from CoreApp.services.utils import ObjectManipulationManager



def getUserAwardsQuery(user):
    """ Возвращает все грамоты user """
    return KvantAward.objects.filter(user=user)


class UserChangeManipulationResponse(ObjectManipulationManager):
    def _constructRedirectUrl(self, obj):
        return rl('profile_page')
