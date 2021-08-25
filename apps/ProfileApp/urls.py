from . import views
from django.urls import path


urlpatterns = [
    path('<int:identifier>/profile', views.ProfilePageTemplateView.as_view(), name='profile_page'),
    path('<int:identifier>/portfolio', views.PortfolioPageTemplateView.as_view(), name='portfolio_page'),
    path('<int:identifier>/statistics', views.StatisticPageTemplateView.as_view(), name='statistic_page'),
]
