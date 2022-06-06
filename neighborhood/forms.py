from django.forms import ModelForm

from neighborhood.models import NeighborhoodPhoto


class NeighborhoodPhotoForm(ModelForm):
    class Meta:
        model = NeighborhoodPhoto
        fields = ['image']
