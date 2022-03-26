from django.urls import path

from . import views

urlpatterns = [
    # Каталог проекта
    path('catalog/', views.ProjectCatalogTemplateView.as_view(), name='project_catalog'),
    path('create/', views.ProjectCreateView.as_view(), name='create_project'),
    
    # Страница проекта
    path('info/<int:project_identifier>', views.ProjectInfoDetailView.as_view(), name='project_info'),
    path('team/<int:project_identifier>', views.ProjectTeamManagerDetailView.as_view(), name='project_team'),
    path('workspace/<int:project_identifier>', views.ProjectWorkspaceDetailView.as_view(), name='project_tasks'),

    # Изменение статуса проекта
    path('hiring/<int:project_identifier>', views.HiringManipulationView.as_view(), name='manipulate_hiring'),
    path('close/<int:project_identifier>', views.ProjectFinishView.as_view(), name='close_project'),
    
    # Функционал заданий
    path('<int:project_identifier>/task/create', views.ProjectTaskCreateView.as_view(), name='create_task'),
    path('<int:project_identifier>/task/status', views.ProjectStatusUpdateView.as_view(), name='task_status'),
    path('<int:project_identifier>/task/info/<int:task_identifier>', views.ProjectTaskDetailView.as_view(), name='task_view'),
    path('<int:project_identifier>/task/update/<int:task_identifier>', views.ProjectTaskUpdateView.as_view(), name='update_task'),

    # Манипуляции командой
    path('<int:project_identifier>/kick', views.KickMemberView.as_view(), name='kick_member'),
    path('<int:project_identifier>/application/create', views.ProjectApplicationSaveView.as_view(), name='create_application'),
    path('<int:project_identifier>/application/manipulate', views.MemberRequestManipulationView.as_view(), name='manipulate_application'),
]
