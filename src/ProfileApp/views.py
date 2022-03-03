from django.views import generic
from . import services
from .models import KvantAward


class SettingsPageTemplateView(generic.TemplateView):
    template_name = 'ProfileApp/SettingsPage/index.html'


class PortfolioPageListView(generic.ListView):
    model               = KvantAward
    context_object_name = 'awards'
    template_name       = 'ProfileApp/PortfolioPage/index.html'

    def get_queryset(self):
        return services.getUserAwardsQuery(self.request.user)


class StaticsPageTemplateView(generic.TemplateView):
    template_name = 'ProfileApp/StatisticsPage/index.html'



