from django import template
from MailApp.models import ImportantMail

register = template.Library()

def get_mail_status(mail, user):
    if mail.sender == user:
        return ''
    return 'new' if not(mail.receivers.all().get(receiver=user).is_read) else ''


def is_important_mail(mail, user):
    return 'active' if ImportantMail.objects.filter(mail=mail, user=user).exists() else ''


register.filter('get_mail_status', get_mail_status)
register.filter('is_important_mail', is_important_mail)
