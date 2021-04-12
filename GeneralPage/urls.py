from . import views
from django.urls import path


urlpatterns = [
    path('test', views.test),
    path('<int:identifier>/main', views.main_page, name='main_page'),
    path('<int:identifier>/send/news', views.send_new_news, name='send_news'),
    path('<int:identifier>/create/news', views.create_new_news, name='create_news'),
    path('<int:identifier>/news/detail/<int:news_identifier>', views.news_detail_view, name='detail_news'),
]
