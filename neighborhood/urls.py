from django.urls import path
from django.views.generic import TemplateView

from .views import (createNeighborhood,
                    showNeighborhoodImages,
                    uploadNeighborhoodImage,
                    deleteNeighborhoodImage,
                    showPointsOfInterest,
                    editNeighborhood,
                    addPointOfInterest,
                    deletePointOfInterest,
                    editPointOfInterest,
                    deletePointOfInterestImage,
                    uploadPointOfInterestImage,
                    showPointOfInterestImages,
                    editNeighborhoodImage,
                    editPointOfInterestImage,
                    neighborhoodProfile,
                    pointOfInterestProfile,
                    )

app_name = 'neighborhood'

urlpatterns = [
    path('neighborhood/information/', createNeighborhood, name='createNeighborhood'),
    path('neighborhood/information/edit/', editNeighborhood, name='editNeighborhood'),
    path('neighborhood/images/', showNeighborhoodImages, name='showNeighborhoodImages'),
    path('neighborhood/images/sw.js', TemplateView.as_view(template_name='sw.js',
                                                           content_type='application/x-javascript')),
    path('neighborhood/<int:pk>/images/upload/', uploadNeighborhoodImage, name='uploadNeighborhoodImage'),
    path('neighborhood/<int:pk>/images/sw.js', TemplateView.as_view(template_name='sw.js',
                                                                    content_type='application/x-javascript')),
    path('neighborhood/image/<int:pk>/delete/', deleteNeighborhoodImage, name='deleteNeighborhoodImage'),
    path('neighborhood/image/<int:pk>/edit/', editNeighborhoodImage, name='editNeighborhoodImage'),
    path('neighborhood/<int:pk>/points_of_interest/add/', addPointOfInterest, name='addPointOfInterest'),
    path('neighborhood/point_of_interest/<int:pk>/edit/', editPointOfInterest, name='editPointOfInterest'),
    path('neighborhood/points_of_interest/', showPointsOfInterest, name='showPointsOfInterest'),
    path('neighborhood/point_of_interest/<int:pk>/delete/', deletePointOfInterest, name='deletePointOfInterest'),
    path('neighborhood/points_of_interest/image/<int:pk>/delete/',
         deletePointOfInterestImage, name='deletePointOfInterestImage'),
    path('neighborhood/point_of_interest/<int:pk>/image/upload/',
         uploadPointOfInterestImage, name='uploadPointOfInterestImage'),

    path('neighborhood/points_of_interest/image/<int:pk>/edit/',
         editPointOfInterestImage, name='editPointOfInterestImage'),

    path('neighborhood/point_of_interest/<int:pk>/images/',
         showPointOfInterestImages, name='showPointOfInterestImages'),
    path('neighborhood/<int:pk>/profile/', neighborhoodProfile, name='neighborhoodProfile'),
    path('point_of_interest/<int:pk>/profile/', pointOfInterestProfile, name='pointOfInterestProfile'),
]
