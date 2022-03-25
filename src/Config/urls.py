from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django_admin/', admin.site.urls),
    path('system/', include('CoreApp.urls')),
    
    path('news/', include('NewsApp.urls')),
    path('mail/', include('MailApp.urls')),
    path('login/', include('LoginApp.urls')),
    path('diary/', include('DiaryApp.urls')),
    path('admin/', include('AdminApp.urls')),
    path('journal/', include('JournalApp.urls')),
    path('profile/', include('ProfileApp.urls')),
    path('projects/', include('ProjectApp.urls')), 
]
