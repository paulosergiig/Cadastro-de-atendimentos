from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('contas/', include('django.contrib.auth.urls')), # URLs de login, logout, etc.
    path('accounts/', include('accounts.urls')),
    path('pacientes/', include('patients.urls')),
]

# Servir arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)