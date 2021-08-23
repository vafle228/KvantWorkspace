from django.urls import path
from .views import LoginPageTemplateView, UserLogInView

urlpatterns = [
	path('', LoginPageTemplateView.as_view(), name='login_page'),
	path('authorization/', UserLogInView.as_view(), name='auth'),
]