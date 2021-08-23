from .models import KvantNews
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import KvantNewsSaveForm
from SystemModule.forms import FileStorageSaveForm
from django.shortcuts import HttpResponse, redirect
from SystemModule.views import KvantJournalAccessMixin


# View для отображения главной страницы
class MainPageTemplateView(KvantJournalAccessMixin, generic.TemplateView):
    template_name = 'NewsApp/MainPage/index.html'
    
    # Метод создания контекста данных
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем представления контекста
        user = self.request.user
        
        from AdminModule.models import KvantCourse
        
        if user.permission == 'Ученик':  # В случаи, если user - ученик, верни его курсы
            context['courses'] = KvantCourse.objects.filter(students__student=user)
        elif user.permission == 'Учитель':  # В случаи, если user - учитель, верни его курсы
            context['courses'] = KvantCourse.objects.filter(teacher__teacher=user)
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
        if request.user.permission == 'Ученик':  # Проверка на права
            return redirect(f'/news/{request.user.id}/main')
        
        form = KvantNewsSaveForm(request.POST, request.FILES)  # Форма создания новости       
        if form.is_valid():               
            news = self.fill_news_files(form.save())  # Добавления файлов в новость
            kwargs = {
                'identifier': request.user.id,
                'news_identifier': news.id,
            }
            return HttpResponse(reverse_lazy('detail_news', kwargs=kwargs))  # Переход на новость
        return HttpResponse(reverse_lazy('main_page', kwargs=kwargs))  # Если был неверный метод

    # Функция для делегирования заполнения новости
    def fill_news_files(self, news):
        date = timezone.now().date()
        for file in self.request.FILES.getlist('files'):  # Добавление файлов в новость
            file_form = FileStorageSaveForm(
                {'upload_path': f'news/files/{date}/{self.request.POST["title"]}'}, {'file': file}
            )  # Создание файла
            if file_form.is_valid():  # Проверка валидности файла
                news.files.add(file_form.save())  # Добавление нового файла
        return news


# View для обновления новости
class NewsUpdateView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        news = KvantNews.objects.get(id=kwargs['news_identifier'])
        if request.user != news.author:  # Проверка на права
            return redirect(f'/news/{request.user.id}/main')
        
        form = KvantNewsSaveForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = self.fill_news_files(form.save())  # Добавления файлов в новость
            kwargs = {
                'identifier': request.user.id,
                'news_identifier': news.id,
            }
            return HttpResponse(reverse_lazy('detail_news', kwargs=kwargs))  # Переход на новость
        return HttpResponse(reverse_lazy('main_page', kwargs={'identifier': request.user.id}))  # Если был неверный метод
    
    # Функция для делегирования заполнения новости
    def fill_news_files(self, news):
        date = timezone.now().date()
        for file in self.request.FILES.getlist('files'):  # Добавление файлов в новость
            file_form = FileStorageSaveForm(
                {'upload_path': f'news/files/{date}/{self.request.POST["title"]}'}, {'file': file}
            )  # Создание файла
            if file_form.is_valid():  # Проверка валидности файла
                news.files.add(file_form.save())  # Добавление нового файла
        return news