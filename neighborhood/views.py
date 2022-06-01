from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry

from registration.models import Neighborhood


def createNeighborhood(request):
    args = {}
    if request.method == 'POST':
        coords = request.POST.get('coordinates')
        print(request.POST.get('neighborhood-name'))
        print(coords.split(',')[0])
        print(len(coords.split(',')))
        final_coords = ""

        for xy in range(0, len(coords.split(',')), 2):
            print('-----------')
            print(coords.split(',')[xy])
            print(coords.split(',')[xy + 1])
            final_coords = final_coords + coords.split(',')[xy] + ' ' + coords.split(',')[xy + 1] + ','

        final_coords = final_coords[:-1]
        print(final_coords)
        neighborhood = Neighborhood()
        neighborhood.name = request.POST.get('neighborhood-name')
        neighborhood.shape = GEOSGeometry('MULTIPOLYGON(((' + final_coords + ')))')
        neighborhood.is_active = False  # TODO - cuándo poner ACTIVO un barrio??
        print(neighborhood.name)
        print("multipolygon!!! ! ! ")
        print(neighborhood.shape)
        # TODO - validar datos?
        neighborhood.save()
        return HttpResponseRedirect('/')

    return render(request, 'create_neighborhood.html', args)
