from django.urls import path
from .views import LoginAppTemplateView


urlpatterns = [
    path('', LoginAppTemplateView.as_view(), name='login_page'),
]