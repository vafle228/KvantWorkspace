from django.views import generic
from django.http import JsonResponse
from LoginApp.models import KvantUser
from core.classes import ModelsFileFiller
from django.shortcuts import HttpResponse
from core.mixins import KvantJournalAccessMixin
from .forms import KvantMailSaveForm, MailReceiverSaveForm
from .models import KvantMessage, ImportantMail, MailReceiver


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
        if self.request.GET.get('type') == 'sent':
            return KvantMessage.objects.filter(sender=self.request.user)
        if self.request.GET.get('type') == 'received':
            return KvantMessage.objects.filter(receivers__receiver=self.request.user)
        if self.request.GET.get('type') == 'importants':
            return KvantMessage.objects.filter(importantmail__user=self.request.user)
        return KvantMessage.objects.none()  # TODO: 404 page return


class MailCreationView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        form = KvantMailSaveForm(self.request.POST)
        if form.is_valid():
            if self.request.POST.getlist('receivers'):
                self.fill_mail_files(form.save(request))
                return JsonResponse({'status': 200, 'link': 'Reload'})
            form.add_error(None, 'Письмо должно содержать хотя бы одного получателя')
        return JsonResponse({'status': 400, 'errors': form.errors})

    def fill_mail_files(self, mail):
        filler = ModelsFileFiller('mail/', mail.files)
        filler.fill_model_files(self.request.FILES.getlist('files'), mail.title)


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
                form = MailReceiverSaveForm({"receiver": request.user, "is_read": True}, instance=receiver)
                form.save() if form.is_valid() else None
        return super().get(request, *args, **kwargs)


class MailChangeImportantStatusView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        if KvantMessage.objects.filter(id=request.POST['id']).exists():
            mail = KvantMessage.objects.get(id=request.POST['id'])
            important_mail, created = ImportantMail.objects.get_or_create(user=request.user, mail=mail)

            important_mail.delete() if not created else None
        return HttpResponse({'status': 200})
