from django.db import models
from cloudinary.models import CloudinaryField

from registration.models import Neighborhood


class NeighborhoodPhoto(models.Model):
    image = CloudinaryField('image')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)

    class Meta:
        db_table = 'neighborhood_photo'
