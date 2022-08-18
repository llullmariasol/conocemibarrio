"""conocemibarrio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from conocemibarrio import settings
from registration.views import send_push
from forum.views import notifications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('registration.urls')),
    path('', include('neighborhood.urls')),
    path('forum/', include('forum.urls')),
    path('notifications/', notifications, name='notifications'),
    path('', include('pwa.urls')),
    path('', include('profile.urls')),
    path('chat/', include('chat.urls')),
    path('send_push', send_push),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    path('', include('realtime_map.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
