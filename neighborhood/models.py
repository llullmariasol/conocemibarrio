from cloudinary.models import CloudinaryField
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from registration.models import Neighborhood


class NeighborhoodImage(models.Model):
    image = CloudinaryField('image')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)
    description = models.CharField(max_length=45)

    class Meta:
        db_table = 'neighborhood_image'


class PointOfInterest(models.Model):
    name = models.CharField(max_length=45)
    location = models.PointField()
    description = models.TextField(default='')
    # TODO - imagenes

    class Meta:
        db_table = 'point_of_interest'


class NeighborhoodPointOfInterest(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, db_constraint=False, null=True)
    # TODO dbconstraint cambiar a true para que aparezca en diagrama????

    class Meta:
        db_table = 'neighborhood_point_of_interest'

