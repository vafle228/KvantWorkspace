from .models import KvantAward
from django.views import generic


class ProfilePageTemplateView(generic.TemplateView):
    template_name = 'ProfileApp/ProfilePage/index.html'


class PortfolioPageTemplateView(generic.TemplateView):
    template_name = 'ProfileApp/PortfolioPage/index.html'


class StatisticPageTemplateView(generic.TemplateView):
    template_name = 'ProfileApp/StatisticPage/index.html'


class PortfolioListView(generic.ListView):
    model                   = KvantAward
    ordering                = ['-id']
    paginate_by             = 10
    template_name           = 'ProfileApp/PortfolioListView/index.html'
    context_object_name     = 'portfolio'
