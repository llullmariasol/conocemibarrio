from cloudinary.models import CloudinaryField
from django.contrib.gis.db import models
from registration.models import Neighborhood


class NeighborhoodImage(models.Model):
    image = CloudinaryField('image')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)
    description = models.TextField(default='')

    class Meta:
        db_table = 'neighborhood_image'

    def __str__(self):
        return self.neighborhood.name + ' | ' + self.description


class PointOfInterest(models.Model):
    name = models.CharField(max_length=45)
    location = models.PointField()
    description = models.TextField(default='')

    class Meta:
        db_table = 'point_of_interest'

    def __str__(self):
        return self.name


class PointOfInterestImage(models.Model):
    image = CloudinaryField('image')
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, db_constraint=False, null=True)
    description = models.TextField(default='')

    class Meta:
        db_table = 'point_of_interest_image'

    def __str__(self):
        return self.point_of_interest.name + ' | ' + self.description


class NeighborhoodPointOfInterest(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False, null=True)
    point_of_interest = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE, db_constraint=False, null=True)

    class Meta:
        db_table = 'neighborhood_point_of_interest'

    def __str__(self):
        return self.neighborhood.name + ' | ' + self.point_of_interest.name


class PointOfInterestDTO:
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    location = []
    description = models.TextField(default='')
