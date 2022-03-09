from re import template
from django.views import generic


class ProjectCatalogTemplateView(generic.TemplateView):
    template_name = 'ProjectApp/ProjectCatalog/index.html'


class ProjectPageTemplateView(generic.TemplateView):
    template_name = 'ProjectApp/ProjectPage/index.html'
