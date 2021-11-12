from .models import KvantNews
from django.views import generic
from .forms import KvantNewsSaveForm
from django.http.response import HttpResponse
from core.mixins import KvantJournalAccessMixin


# View для отображения главной страницы
class MainPageTemplateView(KvantJournalAccessMixin, generic.TemplateView):
    template_name = 'NewsApp/MainPage/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user = self.request.user
        
        from AdminModule.models import KvantCourse
        
        if user.permission == 'Ученик': 
            context['courses'] = KvantCourse.objects.filter(students=user)
        elif user.permission == 'Учитель': 
            context['courses'] = KvantCourse.objects.filter(teacher=user)
        context['max_news'] = len(KvantNews.objects.all())

        return context


# View для детального просмотра новости
class NewsDetailView(KvantJournalAccessMixin, generic.DetailView):
    # TODO добавить cutom 404 page (нужно переписать detail)
    model               = KvantNews
    pk_url_kwarg        = 'news_identifier'
    context_object_name = 'news';
    template_name       = 'NewsApp/NewsDetailView/index.html'


# View для пагинации по новостям
class NewsListView(KvantJournalAccessMixin, generic.ListView):
    model               = KvantNews
    ordering            = ['-date', '-id']
    paginate_by         = 6
    template_name       = 'NewsApp/NewsPreview/index.html'
    context_object_name = 'all_news'


# Базовый класс для манипуляцией новостями
class _NewsManipulationBaseView(generic.View):
    def post(self, request, *args, **kwargs):
        from django.urls import reverse_lazy
        from django.http import JsonResponse

        redirect_kwargs = {'identifier': request.user.id}
        if kwargs.get('is_available'):
            if kwargs.get('form').is_valid():
                redirect_kwargs['news_identifier'] = self.fill_news_files(kwargs.get('form').save()).id
                return JsonResponse({'status': 200, 'link': reverse_lazy('detail_news', kwargs=redirect_kwargs)})
            return JsonResponse({'status': 400, 'errors': kwargs.get('form').errors})  
        return JsonResponse({'status': 403,'link': reverse_lazy('main_page', kwargs=redirect_kwargs)})
    
    def fill_news_files(self, news):
        from core.classes import ModelsFileFiller

        filler = ModelsFileFiller('news/', news.files)
        filler.fill_model_files(self.request.FILES.getlist('files'), news.title)

        return news


# View для создания новости
class NewsCreateView(KvantJournalAccessMixin, _NewsManipulationBaseView, generic.View):    
    def post(self, request, *args, **kwargs):
        post_kwargs = {
            'is_available': request.user.permission != 'Ученик',
            'form': KvantNewsSaveForm(request.POST, request.FILES)
        }
        return super().post(request, *args, **post_kwargs)


# View для обновления новости
class NewsUpdateView(KvantJournalAccessMixin, _NewsManipulationBaseView, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantNews.objects.filter(id=kwargs.get('news_identifier')).exists():
            news = KvantNews.objects.get(id=kwargs.get('news_identifier'))
            post_kwargs = {
                'is_available': request.user == news.author,
                'form': KvantNewsSaveForm(request.POST, request.FILES, instance=news)
            }
            return super().post(request, *args, **post_kwargs)
        return HttpResponse({'status': 404})

# View для удаления новости
class NewsDeleteView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantNews.objects.filter(id=kwargs.get('news_identifier')).exists():
            news = KvantNews.objects.get(id=kwargs.get('news_identifier'))
            if request.POST.get('confirm') and news.author == request.user:
                news.delete()
            return HttpResponse({'status': 200})
        return HttpResponse({'status': 404})