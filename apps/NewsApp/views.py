from .models import KvantNews
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse
from AdminModule.models import KvantCourse
from django.http.response import HttpResponse
from core.mixins import KvantJournalAccessMixin
from .forms import KvantNewsSaveForm, KvantNewsFilesSaveForm


# View для отображения главной страницы
class MainPageTemplateView(KvantJournalAccessMixin, generic.TemplateView):
    template_name = 'NewsApp/MainPage/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        user = self.request.user
        
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


# View для создания новости
class NewsCreateView(KvantJournalAccessMixin, generic.View):    
    def post(self, request, *args, **kwargs):
        redirect_kwargs = {'identifier': request.user.id}
        if request.user.permission != 'Ученик':
            news = None
            forms = [KvantNewsSaveForm, KvantNewsFilesSaveForm]

            for creation_form in forms:
                form = creation_form(
                    request.POST, request.FILES, instance=news
                )
                if not form.is_valid():
                    news.delete() if news else None
                    return JsonResponse({'status': 400, 'errors': form.errors})
                news = form.save()

            redirect_kwargs['news_identifier'] = news.id
            return JsonResponse({'status': 200, 'link': reverse_lazy('detail_news', kwargs=redirect_kwargs)})
        return JsonResponse({'status': 403, 'link': reverse_lazy('main_page', kwargs=redirect_kwargs)})


# View для обновления новости
class NewsUpdateView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        redirect_kwargs = {'identifier': request.user.id}
        if KvantNews.objects.filter(id=kwargs.get('news_identifier')).exists():
            news = KvantNews.objects.get(id=kwargs.get('news_identifier'))
            
            if request.user == news.author:
                forms = [KvantNewsSaveForm, KvantNewsFilesSaveForm]

                for form in range(len(forms)):
                    forms[form] = forms[form](
                        request.POST, request.FILES, instance=news
                    )
                    if not forms[form].is_valid():
                        return JsonResponse({'status': 400, 'errors': forms[form].errors})
                [form.save() for form in forms]
                redirect_kwargs['news_identifier'] = news.id
                return JsonResponse({'status': 200, 'link': reverse_lazy('detail_news', kwargs=redirect_kwargs)})
        return JsonResponse({'status': 403, 'link': reverse_lazy('main_page', kwargs=redirect_kwargs)})
    

# View для удаления новости
class NewsDeleteView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantNews.objects.filter(id=kwargs.get('news_identifier')).exists():
            news = KvantNews.objects.get(id=kwargs.get('news_identifier'))
            if request.POST.get('confirm') and news.author == request.user:
                news.delete()
            return HttpResponse({'status': 200})
        return HttpResponse({'status': 404})