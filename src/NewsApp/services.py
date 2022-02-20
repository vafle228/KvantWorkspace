from CoreApp.services.access import KvantObjectExistsMixin
from django.urls import reverse_lazy as rl
from CoreApp.services.utils import ObjectManupulationResponse

from .models import KvantNews


def getNewsCount():
    """ Возвращает кол-во новостей для ajax пагинации """
    return len(KvantNews.objects.all())


def getNewsById(id):
    """ Вовзращает новость по ее id. """
    return KvantNews.objects.get(id=id)


class NewsObjectManupulationResponse(ObjectManupulationResponse):
    def _getRedirectKwargs(self, request, obj=None):
        if obj is None:
            return {'identifier': request.user.id}
        return {'identifier': request.user.id, 'news_identifier': obj.id}
    
    def _constructRedirectUrl(self, request, obj=None):
        if obj is None:
            return rl('main_page', kwargs=self._getRedirectKwargs(request))
        return rl('detail_news', kwargs=self._getRedirectKwargs(request, obj))


class NewsExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'news_identifier'

    def _objectExiststTest(self, object_id):
        return KvantNews.objects.filter(id=object_id).exists()


class NewsAccessMixin(KvantObjectExistsMixin):
    request_object_arg = 'news_identifier'
    
    def accessTest(self, **kwargs):
        news_id = kwargs.get(self.request_object_arg)
        if self._objectExiststTest(news_id):
            news, user = getNewsById(news_id), kwargs.get('user')
            return self._newsAccessTest(news, user) and super().accessTest(**kwargs)
        return False
    
    def _newsAccessTest(self, news, user):
        """ Тест на авторство """
        return news.author == user
    
    def _objectExiststTest(self, object_id):
        return KvantNews.objects.filter(id=object_id).exists()
