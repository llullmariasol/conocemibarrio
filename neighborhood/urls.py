from django.urls import path

from .views import createNeighborhood

app_name = 'registration'

urlpatterns = [
    path('create_neighborhood/', createNeighborhood, name='createNeighborhood'),
]
