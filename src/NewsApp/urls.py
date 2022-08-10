from django.urls import path

from . import views

urlpatterns = [
    path('send', views.NewsListView.as_view(), name='send_news'),
    path('create', views.NewsCreateView.as_view(), name='create_news'),
    path('main', views.MainPageTemplateView.as_view(), name='main_page'),
    path('create/event', views.EventCreateView.as_view(), name='create_event'),
    path('detail/<int:news_identifier>', views.NewsDetailView.as_view(), name='detail_news'),
    path('update/<int:news_identifier>', views.NewsUpdateView.as_view(), name='update_news'),
    path('delete/<int:news_identifier>', views.NewsDeleteView.as_view(), name='delete_news'),
]
