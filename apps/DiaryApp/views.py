from .models import KvantLesson
from django.views import generic
from core.mixins import KvantJournalAccessMixin


class DiaryPageListView(KvantJournalAccessMixin, generic.ListView):
    model               = KvantLesson
    ordering            = ['-date', '-id']
    template_name       = 'DiaryApp/DiaryPage/index.html'
    context_object_name = 'tasks'

    # def get_queryset(self):
    #     if self.request.GET.get('type') == 'lesson':
    #         return KvantLesson.objects.filter(works__student=self.request.user)
    #     if self.request.GET.get('type') == 'task':
    #         return KvantTask.objects.filter(works__student=self.request.user)
    #     return KvantTask.objects.none()  # TODO: 404 page return