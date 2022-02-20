from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.utils import ObjectManupulationResponse
from django.urls import reverse_lazy as rl
from LoginApp.models import KvantUser

from .forms import MailReceiverSaveForm
from .models import KvantMessage, MailReceiver, ImportantMail


def getMailById(mail_id):
    return KvantMessage.objects.get(id=mail_id)


def makeMailImportant(user, mail_id):
    important_mail, created = ImportantMail.objects.get_or_create(
        user=user, mail=getMailById(mail_id))
    if not created: important_mail.delete() 


class MailBoxQuerySelector:
    """ Класс получения множества писем по type и search """
    def __init__(self, type, search=None):
        self.box_type = type
        self.search_param = search
    
    def getBoxQuery(self, user):
        """
        Получает отфильтрованное множество.
        Если имеется параметр search_param, то фильрует дважды.
        """
        if self.search_param:
            return self._applySearchFilter(self._getMessagesQuery(user))
        return self._getMessagesQuery(user)

    def _getMessagesQuery(self, user):
        """ 
        Фильтрует письма по box_type параметру для пользователя user.
        Если параметр не существует, вовзращает пустое множество.
        """
        box_data = {
            'sent': lambda user: KvantMessage.objects.filter(sender=user),
            'received': lambda user: KvantMessage.objects.filter(receivers__receiver=user),
            'important': lambda user: KvantMessage.objects.filter(importantmail__user=user)}
        if self.box_type in box_data.keys():
            return box_data[self.box_type](user)
        return KvantMessage.objects.none()

    def _applySearchFilter(self, query):
        """ Фильтрует множество по заголовку с title__contains=param """
        return query.filter(title__contains=self.search_param)


class MailObjectManupulationResponse(ObjectManupulationResponse):
    def _getRedirectKwargs(self, request, obj=None):
        return {'identifier': request.user.id}

    def _constructRedirectUrl(self, request, obj=None):
        return rl('mail_box', kwargs=self._getRedirectKwargs(request, obj)) + '?type=received'


class KvantMailAccessMixin(KvantObjectExistsMixin): 
    request_object_arg = 'mail_identifier'

    def accessTest(self, **kwargs):
        mail_id = kwargs.get(self.request_object_arg)
        if self._objectExiststTest(mail_id):
            mail, user = getMailById(mail_id), kwargs.get('user')
            return self._userReceiverTest(user, mail) and super().accessTest(**kwargs)
        return False
    
    def _objectExiststTest(self, object_id):
        return KvantMessage.objects.filter(id=object_id).exists()
    
    def _userReceiverTest(self, user, mail):
        return mail.receivers.filter(receiver=user).exists() or mail.sender == user


class ChangeMailReadStatus:
    def changeReadStatus(self, mail_id, user):
        mail = getMailById(mail_id)
        if mail.receivers.filter(receiver=user).exists():
            return self._saveNewStatus(mail, user)

    def _saveNewStatus(self, mail, user):
        """ Изменяет статус письма на прочитанный. """
        form = MailReceiverSaveForm(
            {"receiver": user, "is_read": True}, 
            instance=mail.receivers.get(receiver=user))
        if form.is_valid(): form.save()


getReceivers = lambda user: KvantUser.objects.exclude(id=user.id)
getSendMails = lambda user: len(KvantMessage.objects.filter(sender=user))
getReceivedMails = lambda user: len(KvantMessage.objects.filter(receivers__receiver=user))
getNewMails = lambda user: len(MailReceiver.objects.filter(receiver=user).filter(is_read=False))
