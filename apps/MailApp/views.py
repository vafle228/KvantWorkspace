from django.views import generic
from django.http import JsonResponse
from LoginApp.models import KvantUser
from core.classes import ModelsFileFiller
from django.shortcuts import HttpResponse
from core.mixins import KvantJournalAccessMixin
from .models import KvantMessage, ImportantMail, MailReceiver
from .forms import KvantMailFillReceiversForm, KvantMailSaveForm, MailReceiverSaveForm


class _MailPageContentBaseView(generic.View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            new_mails=self._count_new_mails(),
            kvant_users=KvantUser.objects.exclude(id=self.request.user.id),
            mail_count=self._count_send_mails() + self._count_received_mails(),
        )
        return context

    def _count_send_mails(self):
        return len(KvantMessage.objects.filter(sender=self.request.user))

    def _count_received_mails(self):
        return len(KvantMessage.objects.filter(receivers__receiver=self.request.user))

    def _count_new_mails(self):
        return len(MailReceiver.objects.filter(receiver=self.request.user).filter(is_read=False))


class MailListView(KvantJournalAccessMixin, _MailPageContentBaseView, generic.ListView):
    model               = KvantMessage
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'MailApp/MailBox/index.html'
    context_object_name = 'mails'

    def get_queryset(self):
        queryset = KvantMessage.objects.none()
        if self.request.GET.get('type') == 'sent':
            queryset = KvantMessage.objects.filter(sender=self.request.user)
        if self.request.GET.get('type') == 'received':
            queryset = KvantMessage.objects.filter(receivers__receiver=self.request.user)
        if self.request.GET.get('type') == 'important':
            queryset = KvantMessage.objects.filter(importantmail__user=self.request.user)
        if self.request.GET.get('search'):
            queryset = queryset.filter(title__contains=self.request.GET.get('search'))
        return queryset


class MailCreationView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        mail_or_error = self.create_mail()
        if isinstance(mail_or_error, KvantMessage):
            self.fill_mail_files(mail_or_error)
            return JsonResponse({'status': 200, 'link': 'Reload'})
        return JsonResponse(mail_or_error)

    def fill_mail_files(self, mail):
        filler = ModelsFileFiller('mail/', mail.files)
        filler.fill_model_files(self.request.FILES.getlist('files'), mail.title)
    
    def create_mail(self):
        form = KvantMailSaveForm(self.request.POST)
        if form.is_valid():
            no_receivers_mail = form.save()
            form = KvantMailFillReceiversForm(
                self.request.POST, instance=no_receivers_mail
            )
            if form.is_valid():
                return form.save()
            no_receivers_mail.delete()
        return {'status': 400, 'errors': form.errors}

class MailDetailView(KvantJournalAccessMixin, generic.DetailView):
    model               = KvantMessage
    pk_url_kwarg        = 'mail_identifier'
    context_object_name = 'mail'
    template_name       = 'MailApp/MailDetailView/index.html'

    def get(self, request, *args, **kwargs):
        if KvantMessage.objects.filter(id=kwargs.get('mail_identifier')).exists():
            mail = KvantMessage.objects.get(id=kwargs.get('mail_identifier'))
            
            if mail.receivers.filter(receiver=request.user).exists():
                receiver = mail.receivers.get(receiver=request.user)
                form = MailReceiverSaveForm(
                    {"receiver": request.user, "is_read": True}, instance=receiver
                )
                form.save() if form.is_valid() else None
        return super().get(request, *args, **kwargs)


class MailChangeImportantStatusView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantMessage.objects.filter(id=request.POST.get('id')).exists():
            mail = KvantMessage.objects.get(id=request.POST.get('id'))
            important_mail, created = ImportantMail.objects.get_or_create(
                user=request.user, mail=mail
            )
            important_mail.delete() if not created else None
            return HttpResponse({'status': 200})
        return HttpResponse({'status': 400})


class MailDeleteView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantMessage.objects.filter(id=request.POST.get('id')).exists() and request.POST.get('confirm'):
            mail = KvantMessage.objects.get(id=request.POST.get('id'))
            mail.delete() if mail.sender == request.user else None
            
            if MailReceiver.objects.filter(kvantmessage=mail, receiver=request.user).exists():
                MailReceiver.objects.get(kvantmessage=mail, receiver=request.user).delete()
            return HttpResponse({'status': 200})
        return HttpResponse({'status': 400})