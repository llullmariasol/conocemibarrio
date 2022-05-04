from django.urls import path, reverse_lazy, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import (registration,
                    activation,
                    logIn,
                    home,
                    logOut,
                    location,
                    joinNeighborhood)

app_name = 'registration'

urlpatterns = [
    path('', home, name='home'),
    path('location/', location, name='location'),
    path('registration/', registration, name='registration'),
    path('activation/<uidb64>/<token>/', activation, name='activation'),
    path('login/', logIn, name='logIn'),
    path('logout/', logOut, name='logOut'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset_form.html',
             email_template_name='password_reset_email.html',
             success_url=reverse_lazy('registration:password_reset_done')),
         name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url=reverse_lazy('registration:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('location/', registration, name='registration'),
    path('join_neighborhood/', joinNeighborhood, name='joinNeighborhood'),
]
