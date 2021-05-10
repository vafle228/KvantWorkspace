from django.urls import path
from . import views

urlpatterns = [
	path('', views.login_page, name='login_page'),
	path('authorization/', views.login_user, name='auth'),
]