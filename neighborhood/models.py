from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from django.contrib.gis.db import models
from django.contrib.auth.models import User
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


class Post(models.Model):  # TODO - BORRAR
    title = models.CharField(max_length=30)
    body = RichTextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    class Meta:
        db_table = 'post'
