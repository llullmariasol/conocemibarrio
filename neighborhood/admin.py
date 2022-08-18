from django.contrib import admin

from neighborhood.models import (NeighborhoodImage, PointOfInterest, NeighborhoodPointOfInterest, PointOfInterestImage)

admin.site.register(NeighborhoodImage)
admin.site.register(PointOfInterest)
admin.site.register(PointOfInterestImage)
admin.site.register(NeighborhoodPointOfInterest)
