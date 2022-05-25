from django.contrib import admin
from .models import (
    Neighborhood,
    UserNeighborhood,
)

# Register your models here.
admin.site.register(Neighborhood)
admin.site.register(UserNeighborhood)
