from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Neighborhood(models.Model):  # TODO - mover a neighborhood package
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.TextField(default='')
    shape = models.MultiPolygonField()
    is_active = models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'neighborhood'


class UserNeighborhood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False,
                                     related_name='neighborhood', null=True)

    class Meta:
        db_table = 'user_neighborhood'
