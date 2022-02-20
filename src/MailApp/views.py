from CoreApp.services.access import KvantWorkspaceAccessMixin
from CoreApp.services.objects import CreateOrUpdateObject
from django.http import HttpResponse
from django.views import generic

from . import services
from .forms import (KvantMailFileSaveForm, KvantMailReceiversForm,
                    KvantMailSaveForm)
from .models import KvantMessage


class MailListView(KvantWorkspaceAccessMixin, generic.ListView):
    model               = KvantMessage
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'MailApp/MailBox/index.html'
    context_object_name = 'mails'

    def get_queryset(self):
        box_type, search = self.request.GET.get('type'), self.request.GET.get('search')
        return services.MailBoxQuerySelector(box_type, search).getBoxQuery(self.request.user)
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            new_mails=services.getNewMails(self.request.user),
            kvant_users=services.getReceivers(self.request.user))
        return context


class MailCreationView(KvantWorkspaceAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        object_creator = CreateOrUpdateObject(
            [KvantMailSaveForm, KvantMailReceiversForm, KvantMailFileSaveForm])
        mail_or_errors = object_creator.createObject(request)
        return services.MailObjectManupulationResponse().getResponse(request, mail_or_errors)


class MailDetailView(services.KvantMailAccessMixin, generic.DetailView):
    model               = KvantMessage
    pk_url_kwarg        = 'mail_identifier'
    context_object_name = 'mail'
    template_name       = 'MailApp/MailDetailView/index.html'

    def get(self, request, *args, **kwargs):
        services.ChangeMailReadStatus().changeReadStatus(
            kwargs.get(self.pk_url_kwarg), request.user)
        return super().get(request, *args, **kwargs)


class MailChangeImportantStatusView(services.KvantMailAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        services.makeMailImportant(
            request.user, kwargs.get('mail_identifier'))
        return HttpResponse({'status': 200}) 


class MailDeleteView(services.KvantMailAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        mail = services.getMailById(kwargs.get('mail_identifier'))
        if mail.sender == request.user: mail.delete()
        else: mail.receivers.filter(receiver=request.user).delete()
        
        return HttpResponse({'status': 200})


# TODO
# 1) Реализовать все pass-классы
# 2) Привентить дневник
# 3) Заставить Вадима написать 404 страницу
# 4) Подумать над системой создания через ajax.
# 5) Придумать что-то с Response классом (связано с 4)
# 6) Микро почистить темплейты (хотя все равно бесить меня будут)
