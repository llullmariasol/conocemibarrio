from django.urls import path

from .views import (createNeighborhood,
                    showNeighborhoodPhotos,
                    uploadNeighborhoodPhoto,
                    deleteNeighborhoodPhoto,
                    showPointsOfInterest,
                    editNeighborhood
                    )

app_name = 'neighborhood'

urlpatterns = [
    path('neighborhood/information/', createNeighborhood, name='createNeighborhood'),
    path('neighborhood/information/edit/', editNeighborhood, name='editNeighborhood'),
    path('neighborhood/photos/', showNeighborhoodPhotos, name='showNeighborhoodPhotos'),
    path('neighborhood/photos/upload/', uploadNeighborhoodPhoto, name='uploadNeighborhoodPhoto'),
    path('neighborhood/photo/<int:pk>/delete/', deleteNeighborhoodPhoto, name='deleteNeighborhoodPhoto'),
    path('neighborhood/points_of_interest/', showPointsOfInterest, name='showPointsOfInterest')
]
