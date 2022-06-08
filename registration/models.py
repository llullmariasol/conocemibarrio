from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Neighborhood(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    shape = models.GeometryField()
    is_active = models.SmallIntegerField()

    class Meta:
        db_table = 'neighborhood'


class UserNeighborhood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, db_constraint=False,
                                     related_name='neighborhood', null=True)

    class Meta:
        db_table = 'user_neighborhood'
