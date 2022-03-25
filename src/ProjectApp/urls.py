from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.ProjectCatalogTemplateView.as_view(), name='project_catalog'),
    path('create/', views.ProjectCreateView.as_view(), name='create_project'),
    
    path('info/<int:project_identifier>', views.ProjectInfoDetailView.as_view(), name='project_info'),
    path('team/<int:project_identifier>', views.ProjectTeamManagerDetailView.as_view(), name='project_team'),
    path('workspace/<int:project_identifier>', views.ProjectWorkspaceDetailView.as_view(), name='project_tasks'),

    path('hiring/<int:project_identifier>', views.HiringManipulationView.as_view(), name='manipulate_hiring'),
    path('close/<int:project_identifier>', views.FinishProject.as_view(), name='close_project'),
    
    
    path('task/create', views.ProjectTaskCreateView.as_view(), name='create_task'),
    path('task/status', views.ProjectStatusUpdateView.as_view(), name='task_status'),
    path('task/info/<int:task_identifier>', views.ProjectTaskDetailView.as_view(), name='task_view'),
    path('task/update/<int:task_identifier>', views.ProjectTaskUpdateView.as_view(), name='update_task'),

    path('kick/<int:project_identifier>', views.KickMemberView.as_view(), name='kick_member'),
    path('application/create', views.ProjectApplicationSaveView.as_view(), name='create_application'),
    path('application/manipulate', views.MemberRequestManipulationView.as_view(), name='manipulate_application'),
]
