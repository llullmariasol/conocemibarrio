from django.contrib.gis.db import models


class NeighborhoodShape(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    shape = models.GeometryField()

    class Meta:
        managed = False
        db_table = 'neighborhood_shape'


