from .models import KvantAward
from django.views import generic
from core.classes import KvantJournalAccessMixin


class ProfilePageTemplateView(generic.TemplateView, KvantJournalAccessMixin):
    template_name = 'ProfileApp/ProfilePage/index.html'


class PortfolioPageTemplateView(generic.TemplateView, KvantJournalAccessMixin):
    template_name = 'ProfileApp/PortfolioPage/index.html'


class StatisticPageTemplateView(generic.TemplateView, KvantJournalAccessMixin):
    template_name = 'ProfileApp/StatisticsPage/index.html'


class PortfolioListView(generic.ListView, KvantJournalAccessMixin):
    model                   = KvantAward
    ordering                = ['-id']
    paginate_by             = 10
    template_name           = 'ProfileApp/PortfolioListView/index.html'
    context_object_name     = 'portfolio'
    
    def get_queryset(self):
        awards_set = super().get_queryset()
        return awards_set.filter(user__id=self.kwargs['identifier'])
