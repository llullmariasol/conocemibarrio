from django.forms import ModelForm

from neighborhood.models import NeighborhoodImage


class NeighborhoodImageForm(ModelForm):
    class Meta:
        model = NeighborhoodImage
        fields = ['image', 'description']
