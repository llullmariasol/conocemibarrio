from django.urls import path

from .views import (createNeighborhood,
                    showNeighborhoodImages,
                    uploadNeighborhoodImage,
                    deleteNeighborhoodImage,
                    showPointsOfInterest,
                    editNeighborhood,
                    addPointOfInterest,
                    deletePointOfInterest,
                    editPointOfInterest,
                    )

app_name = 'neighborhood'

urlpatterns = [
    path('neighborhood/information/', createNeighborhood, name='createNeighborhood'),
    path('neighborhood/information/edit/', editNeighborhood, name='editNeighborhood'),
    path('neighborhood/images/', showNeighborhoodImages, name='showNeighborhoodImages'),
    path('neighborhood/images/upload/', uploadNeighborhoodImage, name='uploadNeighborhoodImage'),
    path('neighborhood/image/<int:pk>/delete/', deleteNeighborhoodImage, name='deleteNeighborhoodImage'),
    path('neighborhood/points_of_interest/add/', addPointOfInterest, name='addPointOfInterest'),
    path('neighborhood/point_of_interest/<int:pk>/edit/', editPointOfInterest, name='editPointOfInterest'),
    path('neighborhood/points_of_interest/', showPointsOfInterest, name='showPointsOfInterest'),
    path('neighborhood/point_of_interest/<int:pk>/delete/', deletePointOfInterest, name='deletePointOfInterest'),
]