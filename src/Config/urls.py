from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('system/', include('CoreApp.urls')),

    path('news/', include('NewsApp.urls')),
    path('mail/', include('MailApp.urls')),
    path('login/', include('LoginApp.urls')),
    path('diary/', include('DiaryApp.urls')),
    path('journal/', include('JournalApp.urls')),
]
