import json

import cloudinary
from cloudinary.models import CloudinaryField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry

from neighborhood.forms import NeighborhoodImageForm
from neighborhood.models import NeighborhoodImage, PointOfInterest, NeighborhoodPointOfInterest
from registration.models import Neighborhood


def createNeighborhood(request):
    args = {}
    if request.method == 'POST':
        coords = request.POST.get('coordinates')
        final_coords = ""

        for xy in range(0, len(coords.split(',')), 2):
            final_coords = final_coords + coords.split(',')[xy] + ' ' + coords.split(',')[xy + 1] + ','

        final_coords = final_coords[:-1]
        neighborhood = Neighborhood()
        neighborhood.name = request.POST.get('neighborhood-name')
        neighborhood.shape = GEOSGeometry('MULTIPOLYGON(((' + final_coords + ')))')
        neighborhood.is_active = True
        neighborhood.user = request.user
        neighborhood.description = request.POST.get('neighborhood-description')
        neighborhood.save()
        return HttpResponseRedirect('/')

    return render(request, 'create_neighborhood.html', args)


def editNeighborhood(request):
    neighborhood = Neighborhood.objects.filter(user=request.user).first()
    args = {}
    shape = GEOSGeometry(neighborhood.shape)
    input_string = shape.geojson
    coordinates_data = json.loads(input_string)
    args['neighborhood_coords'] = coordinates_data['coordinates'][0][0]
    args['neighborhood'] = neighborhood

    if request.method == 'POST':
        coords = request.POST.get('coordinates')
        final_coords = ""

        for xy in range(0, len(coords.split(',')), 2):
            final_coords = final_coords + coords.split(',')[xy] + ' ' + coords.split(',')[xy + 1] + ','

        final_coords = final_coords[:-1]
        neighborhood.name = request.POST.get('neighborhood-name')
        neighborhood.shape = GEOSGeometry('MULTIPOLYGON(((' + final_coords + ')))')
        neighborhood.is_active = True
        neighborhood.user = request.user
        neighborhood.description = request.POST.get('neighborhood-description')
        neighborhood.save()
        return HttpResponseRedirect('/')

    return render(request, 'edit_neighborhood.html', args)


def showNeighborhoodImages(request):
    n = Neighborhood.objects.get(user_id=request.user)
    images = NeighborhoodImage.objects.all().filter(neighborhood=n)
    print(images)
    return render(request, 'neighborhood_images.html', {'images': images, 'neighborhood': n, })


def uploadNeighborhoodImage(request):
    context = dict(backend_form=NeighborhoodImageForm())

    if request.method == 'POST':
        desc = request.POST.get('image-description')
        archivo = request.FILES['image-file']

        n = Neighborhood.objects.get(user_id=request.user)
        neighborhood_image = NeighborhoodImage()
        neighborhood_image.neighborhood = n
        neighborhood_image.image = archivo
        neighborhood_image.description = desc
        neighborhood_image.save()
        # form = NeighborhoodImageForm(request.POST, request.FILES)
        # context['posted'] = form.instance
        #
        # if form.is_valid():
        #     # image-file
        #     # image-description
#
        #     n = Neighborhood.objects.get(user_id=request.user)
        #     neighborhood_image = NeighborhoodImage()
        #     neighborhood_image.image = form.cleaned_data['image']
        #     neighborhood_image.neighborhood = n
        #     neighborhood_image.save()
        return HttpResponseRedirect('/neighborhood/images/')

    return render(request, 'upload_neighborhood_image.html', context)


def deleteNeighborhoodImage(request, pk):
    image = NeighborhoodImage.objects.get(pk=pk)
    image.delete()
    cloudinary.uploader.destroy(image.image.public_id, invalidate=True)
    return HttpResponseRedirect('/neighborhood/images/')


def addPointOfInterest(request):
    if request.method == 'POST':
        point = request.POST.get('point').split(',')

        point_of_interest = PointOfInterest()
        point_of_interest.name = request.POST.get('point-name')
        point_of_interest.location = GEOSGeometry('POINT(' + point[0] + ' ' + point[1] + ')')
        point_of_interest.save()

        neighborhood_point_of_interest = NeighborhoodPointOfInterest()
        neighborhood_point_of_interest.neighborhood = Neighborhood.objects.filter(user=request.user).first()
        neighborhood_point_of_interest.point_of_interest = point_of_interest
        neighborhood_point_of_interest.save()

        return HttpResponseRedirect('/neighborhood/points_of_interest/')

    return render(request, 'add_point_of_interest.html')


def editPointOfInterest(request, pk):
    args = {}
    point_of_interest = PointOfInterest.objects.get(pk=pk)

    neighborhood = Neighborhood.objects.filter(user=request.user).first()
    args = {}
    location = GEOSGeometry(point_of_interest.location)
    input_string = location.geojson
    coordinates_data = json.loads(input_string)
    print('COOOOOOOOOOORD')
    print(coordinates_data)
    args['coordinates'] = coordinates_data['coordinates']
    args['point'] = point_of_interest

    if request.method == 'POST':
        # TODO - si no tiene nada, es porque no cambió la ubicación, queda =, VALIDAR LO MISMO EN BARRIO
        coords = request.POST.get('point-coordinates')

        if coords is not None:
            print("COORDS DEL POINT")
            print(coords)
        else:
            print("COORDS DEL POINT ----> NONE")

        final_coords = ""


        for xy in range(0, len(coords.split(',')), 2):
            final_coords = final_coords + coords.split(',')[xy] + ' ' + coords.split(',')[xy + 1] + ','

        final_coords = final_coords[:-1]
        neighborhood.name = request.POST.get('neighborhood-name')
        neighborhood.shape = GEOSGeometry('MULTIPOLYGON(((' + final_coords + ')))')
        neighborhood.is_active = True
        neighborhood.user = request.user
        neighborhood.description = request.POST.get('neighborhood-description')
        neighborhood.save()
        return HttpResponseRedirect('/')

    return render(request, 'edit_point_of_interest.html', args)

    #if request.method == 'POST':
    #    point = request.POST.get('point').split(',')
#
    #    point_of_interest = PointOfInterest()
    #    point_of_interest.name = request.POST.get('point-name')
    #    point_of_interest.location = GEOSGeometry('POINT(' + point[0] + ' ' + point[1] + ')')
    #    point_of_interest.save()
#
    #    neighborhood_point_of_interest = NeighborhoodPointOfInterest()
    #    neighborhood_point_of_interest.neighborhood = Neighborhood.objects.filter(user=request.user).first()
    #    neighborhood_point_of_interest.point_of_interest = point_of_interest
    #    neighborhood_point_of_interest.save()
#
    #    return HttpResponseRedirect('/neighborhood/points_of_interest/')

   # return render(request, 'add_point_of_interest.html')


def showPointsOfInterest(request):
    n = Neighborhood.objects.get(user_id=request.user)
    points_of_interest = NeighborhoodPointOfInterest.objects.all().filter(neighborhood=n)
    return render(request, 'neighborhood_points_of_interest.html',
                  {'points': points_of_interest, 'neighborhood': n, })


def deletePointOfInterest(request, pk):
    point_of_interest = PointOfInterest.objects.get(pk=pk)
    point_of_interest.delete()
    return HttpResponseRedirect('/neighborhood/points_of_interest/')
