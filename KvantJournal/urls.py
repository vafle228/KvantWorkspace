from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('NewsApp.urls')),
    path('mail/', include('MailApp.urls')),
    path('login/', include('LoginApp.urls')),
    path('diary/', include('DiaryApp.urls')),

    path('change/theme/', include('SystemModule.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
