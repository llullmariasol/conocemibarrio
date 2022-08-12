import json

from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render

from neighborhood.models import (PointOfInterest, PointOfInterestDTO)


def showRealTimeMap(request):
    args = {}
    points_of_interest = list(PointOfInterest.objects.all())
    points = []

    for point in points_of_interest:
        point_dto = PointOfInterestDTO()
        point_dto.id = point.pk
        point_dto.name = point.name
        point_dto.description = point.description
        point_dto.location = getCoordsArray(point.location)
        points.append(point_dto)

    args['points'] = points

    return render(request, 'realtime_map.html', args)


def getCoordsArray(location):
    geo_location = GEOSGeometry(location)
    input_string = geo_location.geojson
    coordinates_data = json.loads(input_string)
    return coordinates_data['coordinates']
