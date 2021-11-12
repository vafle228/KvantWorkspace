from .models import KvantLesson
from django.views import generic
from core.mixins import KvantJournalAccessMixin


class DiaryPageListView(KvantJournalAccessMixin, generic.ListView):
    model               = KvantLesson
    ordering            = ['-date', '-id']
    template_name       = 'DiaryApp/DiaryPage/index.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        if self.request.user.permission == "Ученик":
            return KvantLesson.objects.filter(course__students__id=self.request.user.id)
        return KvantLesson.objects.filter(course__teacher=self.request.user)


class DiaryLessonDetailView(KvantJournalAccessMixin, generic.DetailView):
    model               = KvantLesson
    pk_url_kwarg        = 'lesson_identifier'
    context_object_name = 'lesson'
    template_name       = 'DiaryApp/LessonDetailView/index.html'
