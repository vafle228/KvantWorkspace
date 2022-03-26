from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl

from .models import KvantNews


def getNewsCount():
    """ Возвращает кол-во новостей для ajax пагинации """
    return len(KvantNews.objects.all())


def getNewsById(id):
    """ Вовзращает новость по ее id. """
    return KvantNews.objects.get(id=id)


class NewsObjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, **kwargs):
        return rl('detail_news', kwargs={'news_identifier': kwargs.get('obj').id})


class NewsExistsMixin(KvantObjectExistsMixin):
    request_object_arg = 'news_identifier'

    def _objectExiststTest(self, object_id):
        return KvantNews.objects.filter(id=object_id).exists()


class NewsAccessMixin(NewsExistsMixin):
    request_object_arg = 'news_identifier'
    
    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            news = getNewsById(kwargs.get(self.request_object_arg))
            return self._newsAccessTest(news, kwargs.get('user')) 
        return False
    
    def _newsAccessTest(self, news, user):
        """ Тест на авторство """
        return news.author == user
