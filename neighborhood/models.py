from django.contrib.gis.db import models
from cloudinary.models import CloudinaryField

from registration.models import Neighborhood


class NeighborhoodPhoto(models.Model):
    image = CloudinaryField('image')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)

    class Meta:
        db_table = 'neighborhood_photo'


class PointOfInterest(models.Model):
    name = models.CharField(max_length=45)
    location = models.PointField()
    # TODO - agregar otros campos

    class Meta:
        db_table = 'point_of_interest'


class NeighborhoodPointOfInterest(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, db_constraint=False, null=True)

    class Meta:
        db_table = 'neighborhood_point_of_interest'
