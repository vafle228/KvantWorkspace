from django.contrib import admin
from .models import KvantMessage, MailReceiver, ImportantMail


admin.site.register(KvantMessage)
admin.site.register(MailReceiver)
admin.site.register(ImportantMail)
