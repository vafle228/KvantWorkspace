from .models import KvantAward


def getUserAwardsQuery(user):
    """ Возвращает все грамоты user """
    return KvantAward.objects.filter(user=user)
