from . import views
from django.urls import path

urlpatterns = [
    path('logout', views.LogoutKvantUserView.as_view(), name='logout_user'),
    
    path('portfolio/add', views.PortfolioAddForm.as_view(), name='add_portfolio'),
    path('<int:user_identifier>/update', views.KvantUserChangeView.as_view(), name='update_user'),
    path('<int:user_identifier>/password', views.PasswordChangeView.as_view(), name='change_password'),

    path('<int:user_identifier>/info', views.SettingsPageTemplateView.as_view(), name='info_page'),
    path('<int:user_identifier>/portfolio', views.PortfolioPageListView.as_view(), name='portfolio_page'),
    path('<int:user_identifier>/projects', views.ProjectsPageTemplateView.as_view(), name='projects_page'),
    path('<int:user_identifier>/statistics', views.StaticsPageTemplateView.as_view(), name='statistics_page'),
]
