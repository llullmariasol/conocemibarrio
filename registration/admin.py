from django.contrib import admin
from .models import (
    Neighborhood,
    UserNeighborhood,
)

admin.site.register(Neighborhood)
admin.site.register(UserNeighborhood)
