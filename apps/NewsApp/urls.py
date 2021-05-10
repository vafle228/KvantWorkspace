from . import views
from django.urls import path


urlpatterns = [
    path('<int:identifier>/main', views.main_page, name='main_page'),
    path('<int:identifier>/send', views.send_new_news, name='send_news'),
    path('<int:identifier>/create', views.create_new_news, name='create_news'),
    path('<int:identifier>/detail/<int:news_identifier>', views.news_detail_view, name='detail_news'),
]
