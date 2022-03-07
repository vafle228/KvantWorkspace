from CoreApp.services.access import KvantWorkspaceAccessMixin
from django.http import HttpResponse
from django.views import generic

from . import services
from .forms import (KvantMailFileSaveForm, KvantMailReceiversForm,
                    KvantMailSaveForm)
from .models import KvantMessage


class MailListView(KvantWorkspaceAccessMixin, generic.ListView):
    """ Контроллер почтовой страницы """
    model               = KvantMessage
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'MailApp/MailBox/index.html'
    context_object_name = 'mails'

    def get_queryset(self):
        return services.MailBoxQuerySelector(
            self.request.GET.get('type'), 
            self.request.GET.get('search')
        ).getBoxQuery(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            new_mails=services.getNewMails(self.request.user),
            kvant_users=services.getReceivers(self.request.user))
        return context


class MailCreationView(KvantWorkspaceAccessMixin, generic.View):
    """ Контроллер создания письма """
    def post(self, request, *args, **kwargs):
        object_manager = services.MailObjectManipulationManager(
            [KvantMailSaveForm, KvantMailReceiversForm, KvantMailFileSaveForm])
        return object_manager.createObject(request)


class MailDetailView(services.KvantMailAccessMixin, generic.DetailView):
    """ Контроллер чтения писем """
    model               = KvantMessage
    pk_url_kwarg        = 'mail_identifier'
    context_object_name = 'mail'
    template_name       = 'MailApp/MailDetailView/index.html'

    def get(self, request, *args, **kwargs):
        services.ChangeMailReadStatus().changeReadStatus(
            kwargs.get(self.pk_url_kwarg), request.user)
        return super().get(request, *args, **kwargs)


class MailChangeImportantStatusView(services.KvantMailAccessMixin, generic.View):
    """ Контроллер пометки важных писем """
    def post(self, request, *args, **kwargs):
        services.makeMailImportant(request.user, kwargs.get('mail_identifier'))
        return HttpResponse({'status': 200}) 


class MailDeleteView(services.KvantMailAccessMixin, generic.View):
    """ Контроллер удаления писем """
    def post(self, request, *args, **kwargs):
        mail = services.getMailById(kwargs.get('mail_identifier'))
        if mail.sender == request.user: mail.delete()
        else: mail.receivers.filter(receiver=request.user).delete()
        
        return HttpResponse({'status': 200})
