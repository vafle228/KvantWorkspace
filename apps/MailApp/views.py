from django.http import JsonResponse
from LoginApp.models import KvantUser
from core.mixins import KvantJournalAccessMixin

from .models import KvantMessage, ImportantMail, MailReceiver
from .forms import KvantMailSaveForm
from django.shortcuts import render, redirect, HttpResponse
from django.views import generic


class MailListView(KvantJournalAccessMixin, generic.ListView):
    model               = KvantMessage
    ordering            = ['-date', '-id']
    paginate_by         = 8
    template_name       = 'MailApp/MailBox/index.html'
    context_object_name = 'mails'
    
    def get_queryset(self):
        mails_type = self.request.GET['type']

        if mails_type == 'sent':
            return KvantMessage.objects.filter(sender=self.request.user)
        if mails_type == 'received':
            return KvantMessage.objects.filter(receivers__receiver=self.request.user)
        if mails_type == 'important':
            return KvantMessage.objects.filter(importantmail__user=self.request.user)
        return KvantMessage.objects.none()
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        send_mails = len(KvantMessage.objects.filter(sender=self.request.user))
        received_mails = len(KvantMessage.objects.filter(receivers__receiver=self.request.user))

        context.update(
            box_type=self.request.GET['type'],
            mail_count=send_mails + received_mails,
            kvant_users=KvantUser.objects.exclude(id=self.request.user.id),
            new_mails=len(MailReceiver.objects.filter(receiver=self.request.user).filter(is_read=False)),
        )
        return context


class MailCreationView(KvantJournalAccessMixin, generic.View):
    def post(self, request, *args, **kwargs):
        from django.urls import reverse_lazy

        redirect_kwarg = {
            "identifier": self.request.user.id
        }

        form = KvantMailSaveForm(self.request.POST)
        if form.is_valid():
            redirect_kwarg['mail_identifier'] = self.fill_mail_files(form.save(request)).id
            return JsonResponse({'status': 200, 'link': reverse_lazy('mail_detail', kwargs=redirect_kwarg)})
        if self.request.FILES.getlist('files') == []:
            form.add_error(None, 'Письмо должно содержать хотя бы одного получателя')
        return JsonResponse({'status': 400, 'errors': form.errors})
    

    def fill_mail_files(self, mail):
        from core.classes import ModelsFileFiller
        
        filler = ModelsFileFiller('mail/', mail.files)
        filler.fill_model_files(self.request.FILES.getlist('files'), mail.title)

        return mail


class MailDetailView(KvantJournalAccessMixin, generic.DetailView):
    model               = KvantMessage
    pk_url_kwarg        = 'mail_identifier'
    context_object_name = 'mail'
    template_name       = 'MailApp/MailDetailView/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        send_mails = len(KvantMessage.objects.filter(sender=self.request.user))
        received_mails = len(KvantMessage.objects.filter(receivers__receiver=self.request.user))

        context.update(
            mail_count=send_mails + received_mails,
            kvant_users=KvantUser.objects.exclude(id=self.request.user.id),
            new_mails=len(MailReceiver.objects.filter(receiver=self.request.user).filter(is_read=False)),
        )
        return context 


# def change_read_status(request, identifier):
#     if request.method == 'POST':
#         mail_id = request.POST['mail_id']  # id письма из запроса

#         if not KvantMessage.objects.filter(id=mail_id).exists():
#             return HttpResponse('Error')

#         mail = KvantMessage.objects.get(id=mail_id)  # Получаем письмо по id

#         # Проверка пользователя на получателя
#         if mail.receivers.all().filter(receiver=request.user).exists():
#             receiver = mail.receivers.all().filter(receiver=request.user)[0]  # Получатель
#             receiver.is_read = True  # Меняем статус
#             receiver.save()  # Перезаписываем
#             return HttpResponse('Ok')
#     return HttpResponse('Error')


# def change_important_status(request, identifier):
#     if request.method == 'POST':
#         mail_id = request.POST['mail_id']

#         if not KvantMessage.objects.filter(id=mail_id).exists():
#             return HttpResponse('Error')

#         mail = KvantMessage.objects.get(id=mail_id)
#         important_mail, created = ImportantMail.objects.get_or_create(user=request.user, mail=mail)
#         if not created:
#             important_mail.delete()
#         return HttpResponse('Ok')
#     return HttpResponse('Error')
