from django.http import HttpResponse
from django.views import generic

from .services import NotificationAccessMixin, deleteNotification


class NotificationDeleteView(NotificationAccessMixin, generic.View):
    def dispatch(self, request, *args, **kwargs):
        kwargs.update(notification_identifier=request.POST.get('notification_identifier'))
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        deleteNotification(request.POST.get('notification_identifier'))
        return HttpResponse('Ok')
