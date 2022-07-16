from django.urls import path
from .views import profile

app_name = 'profile'

urlpatterns = [
    # Add this
    path('profile/', profile, name='users-profile'),
]
