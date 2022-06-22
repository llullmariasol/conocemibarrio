from django.forms import ModelForm

from neighborhood.models import (NeighborhoodImage, PointOfInterestImage)


class NeighborhoodImageForm(ModelForm):
    class Meta:
        model = NeighborhoodImage
        fields = ['image', 'description']


class PointOfInterestImageForm(ModelForm):
    class Meta:
        model = PointOfInterestImage
        fields = ['image', 'description']
