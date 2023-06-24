
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from elearning_app.admin import auxilliary_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aux_admin/', auxilliary_admin_site.urls),
    path('', include('elearning_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('messages/', include('django_messages.urls')),
    path('quiz/', include('quiz.urls')),
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)