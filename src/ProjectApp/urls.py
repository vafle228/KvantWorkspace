from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.ProjectCatalogTemplateView.as_view(), name='project_catalog'),
    
    path('info/<int:project_identifier>', views.ProjectInfoDetailView.as_view(), name='project_info'),
    
    path('task/info/<int:task_identifier>', views.ProjectTaskDetailView.as_view(), name='task_view'),
    path('task/update/<int:task_identifier>', views.ProjectTaskUpdateView.as_view(), name='update_task'),
    path('task/create/<int:project_identifier>', views.ProjectTaskCreateView.as_view(), name='create_task'),
    
    path('workspace/<int:project_identifier>', views.ProjectWorkspaceDetailView.as_view(), name='project_tasks'),
]
