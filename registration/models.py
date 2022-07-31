from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Neighborhood(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(default='', null=True, blank=True)
    shape = models.MultiPolygonField(default='', blank=True, null=True)
    is_active = models.SmallIntegerField()

    class Meta:
        db_table = 'neighborhood'


class UserNeighborhood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False,
                                     related_name='neighborhood', null=True)
    justification = models.TextField(default='', null=True)
    rejected = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'user_neighborhood'
