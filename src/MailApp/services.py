from CoreApp.services.access import KvantObjectExistsMixin
from CoreApp.services.utils import ObjectManipulationManager
from django.urls import reverse_lazy as rl
from LoginApp.models import KvantUser

from .forms import MailReceiverSaveForm
from .models import ImportantMail, KvantMessage, MailReceiver


def getMailById(mail_id):
    """ Получает письмо по его id """
    return KvantMessage.objects.get(id=mail_id)


def makeMailImportant(user, mail_id):
    """ Создает экземпляр избранного письма """
    important_mail, created = ImportantMail.objects.get_or_create(
        user=user, mail=getMailById(mail_id))
    if not created: important_mail.delete() 


class MailBoxQuerySelector:
    """ Класс получения множества писем по box_type и search """
    def __init__(self, box_type, search=None):
        self.box_type = box_type
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


class MailObjectManipulationManager(ObjectManipulationManager):
    def _constructRedirectUrl(self, obj):
        return rl('mail_box') + '?type=received'


class KvantMailAccessMixin(KvantObjectExistsMixin): 
    request_object_arg = 'mail_identifier'

    def accessTest(self, **kwargs):
        if super().accessTest(**kwargs):
            mail = getMailById(kwargs.get(self.request_object_arg))
            return self._userReceiverTest(kwargs.get('user'), mail) 
        return False
    
    def _objectExiststTest(self, object_id):
        return KvantMessage.objects.filter(id=object_id).exists()
    
    def _userReceiverTest(self, user, mail):
        return mail.receivers.filter(receiver=user).exists() or mail.sender == user


class ChangeMailReadStatus:
    """ Изменяет статус письма на "прочитан" при необходимости """
    def changeReadStatus(self, mail_id, user):
        mail = getMailById(mail_id)
        if self._canRead(mail, user):
            return self._saveNewStatus(mail, user)
    
    def _canRead(self, mail, user):
        """ Проверяет возможность чтения на основе его статуса """
        if mail.sender != user:
            return not mail.receivers.get(receiver=user).is_read 
        return False

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
