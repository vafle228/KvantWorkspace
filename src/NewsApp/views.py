from django.http import JsonResponse
from CoreApp.services.access import (KvantTeacherAndAdminAccessMixin,
                                     KvantWorkspaceAccessMixin)
from django.views import generic

from . import services
from .forms import KvantNewsFilesSaveForm, KvantNewsSaveForm
from .models import KvantNews
from AdminApp.services import getCourseQuery


class MainPageTemplateView(KvantWorkspaceAccessMixin, generic.TemplateView):
    """ Контроллер главной новостной страницы """
    template_name = 'NewsApp/MainPage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'max_news': services.getNewsCount(),
            'courses': getCourseQuery(self.request.user),
            'events': services.getNewsByType(news_type=True),})
        return context


class NewsDetailView(services.NewsExistsMixin, generic.DetailView):
    """ Контроллер детального просмотра новостей """
    model               = KvantNews
    pk_url_kwarg        = 'news_identifier'
    context_object_name = 'news'
    template_name       = 'NewsApp/NewsDetailView/index.html'


class NewsListView(KvantWorkspaceAccessMixin, generic.ListView):
    """ Контроллер для организации пагинации по новостям """
    model               = KvantNews
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'NewsApp/NewsPreview/index.html'
    context_object_name = 'all_news'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(all_news=services.getNewsByType(news_type=False),)
        return ctx


class NewsCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    """ Контроллер создания новости """
    def post(self, request, *args, **kwargs):
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm])
        return object_manager.createObject(request)

class NewsUpdateView(services.NewsAccessMixin, generic.View):
    """ Контроллер редактирования новости """
    def post(self, request, *args, **kwargs):
        news = services.getNewsById(kwargs.get('news_identifier'))
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm], object=news)
        return object_manager.updateObject(request)


class NewsDeleteView(services.NewsAccessMixin, generic.View):
    """ Контроллер удаления новости """
    def post(self, request, *args, **kwargs):
        services.getNewsById(kwargs.get('news_identifier')).delete()
        return JsonResponse({'status': 200})


class EventCreateView(KvantTeacherAndAdminAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_manager = services.NewsObjectManipulationManager(
            [KvantNewsSaveForm, KvantNewsFilesSaveForm])
        return services.createNewEvent(object_manager, request)
        