from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectCatalogTemplateView.as_view(), name='project_catalog'),
    path('project/', views.ProjectPageTemplateView.as_view(), name='project_page'),
]
