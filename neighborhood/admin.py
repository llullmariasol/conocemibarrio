from django.contrib import admin

from neighborhood.models import (NeighborhoodImage, PointOfInterest, NeighborhoodPointOfInterest)

admin.site.register(NeighborhoodImage)
admin.site.register(PointOfInterest)
admin.site.register(NeighborhoodPointOfInterest)
