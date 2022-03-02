from django.urls import path

from .views import *


# URLs для журнала
urlpatterns = [
    path('', JournalPageTemplateView.as_view(), name='journal_page'),
    
    path('journal/get', JournalDetailView.as_view(), name='journal_view'),
    path('journal/create', CreateTaskView.as_view(), name='create_task'),
    path('update/<int:base_identifier>', UpdateBaseView.as_view(), name='update_base'),
    
    path('check/<int:base_identifier>', CheckingPageDetailView.as_view(), name='checking_page'),
    path('marks/<int:base_identifier>', UpdateMarksView.as_view(), name='update_marks'), 
]
