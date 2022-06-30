import json

import cloudinary
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry

from neighborhood.forms import NeighborhoodImageForm, PointOfInterestImageForm
from neighborhood.models import NeighborhoodImage, PointOfInterest, NeighborhoodPointOfInterest, PointOfInterestImage
from registration.models import Neighborhood, UserNeighborhood


def createNeighborhood(request):
    args = {}
    user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
    neighborhood = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    args['name'] = neighborhood.name
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

    return render(request, 'create_neighborhood.html', args)


def editNeighborhood(request):
    args = {}
    user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
    neighborhood = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    shape = GEOSGeometry(neighborhood.shape)
    input_string = shape.geojson
    coordinates_data = json.loads(input_string)
    args['coordinates'] = coordinates_data['coordinates'][0][0]
    args['neighborhood'] = neighborhood

    if request.method == 'POST':
        coords = request.POST.get('coordinates')

        if coords == '':
            neighborhood.name = request.POST.get('neighborhood-name')
            neighborhood.description = request.POST.get('neighborhood-description')
        else:
            final_coords = ""

            for xy in range(0, len(coords.split(',')), 2):
                final_coords = final_coords + coords.split(',')[xy] + ' ' + coords.split(',')[xy + 1] + ','

            final_coords = final_coords[:-1]
            neighborhood.name = request.POST.get('neighborhood-name')
            neighborhood.shape = GEOSGeometry('MULTIPOLYGON(((' + final_coords + ')))')
            neighborhood.description = request.POST.get('neighborhood-description')

        neighborhood.save()

        return HttpResponseRedirect('/')

    return render(request, 'edit_neighborhood.html', args)


def showNeighborhoodImages(request):
    images = None
    user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
    n = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    # n = Neighborhood.objects.all().filter(user_id=request.user).first()
    if n is not None:
        images = NeighborhoodImage.objects.all().filter(neighborhood=n)
    return render(request, 'neighborhood_images.html', {'images': images, 'neighborhood': n, })


def showPointOfInterestImages(request, pk):
    point_of_interest = PointOfInterest.objects.get(pk=pk)
    images = PointOfInterestImage.objects.all().filter(point_of_interest=point_of_interest)
    return render(request,
                  'point_of_interest_images.html', {'images': images, 'point': point_of_interest, })


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

        return HttpResponseRedirect('/neighborhood/images/')

    return render(request, 'upload_neighborhood_image.html', context)


def editNeighborhoodImage(request, pk):
    args = {}
    image = NeighborhoodImage.objects.get(pk=pk)
    args['image'] = image

    if request.method == 'POST':
        image.description = request.POST.get('image-description')
        image.save()

        return HttpResponseRedirect('/neighborhood/images/')

    return render(request, 'edit_neighborhood_image.html', args)


def deleteNeighborhoodImage(request, pk):
    image = NeighborhoodImage.objects.get(pk=pk)
    image.delete()
    cloudinary.uploader.destroy(image.image.public_id, invalidate=True)
    return HttpResponseRedirect('/neighborhood/images/')


def addPointOfInterest(request):
    args = {}
    neighborhood = Neighborhood.objects.filter(user=request.user).first()
    shape = GEOSGeometry(neighborhood.shape)
    input_string = shape.geojson
    coordinates_data = json.loads(input_string)
    args['coordinates'] = coordinates_data['coordinates'][0][0]

    if request.method == 'POST':
        point = request.POST.get('point').split(',')

        point_of_interest = PointOfInterest()
        point_of_interest.name = request.POST.get('point-name')
        point_of_interest.description = request.POST.get('point-description')
        point_of_interest.location = GEOSGeometry('POINT(' + point[0] + ' ' + point[1] + ')')
        point_of_interest.save()

        neighborhood_point_of_interest = NeighborhoodPointOfInterest()
        neighborhood_point_of_interest.neighborhood = Neighborhood.objects.filter(user=request.user).first()
        neighborhood_point_of_interest.point_of_interest = point_of_interest
        neighborhood_point_of_interest.save()

        return HttpResponseRedirect('/neighborhood/points_of_interest/')

    return render(request, 'add_point_of_interest.html', args)


def editPointOfInterest(request, pk):
    args = {}
    point_of_interest = PointOfInterest.objects.get(pk=pk)
    location = GEOSGeometry(point_of_interest.location)
    input_string = location.geojson
    coordinates_data = json.loads(input_string)
    args['coordinates'] = coordinates_data['coordinates']
    args['point'] = point_of_interest

    user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
    neighborhood = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    # neighborhood = Neighborhood.objects.filter(user=request.user).first()
    shape = GEOSGeometry(neighborhood.shape)
    input_string_shape = shape.geojson
    coordinates_data_neighborhood = json.loads(input_string_shape)
    args['coordinates_neighborhood'] = coordinates_data_neighborhood['coordinates'][0][0]

    if request.method == 'POST':
        coords = request.POST.get('point')
        if coords == '':
            point_of_interest.name = request.POST.get('point-name')
            point_of_interest.description = request.POST.get('point-description')
        else:
            point_of_interest.name = request.POST.get('point-name')
            point_of_interest.description = request.POST.get('point-description')
            point = request.POST.get('point').split(',')
            point_of_interest.location = GEOSGeometry('POINT(' + point[0] + ' ' + point[1] + ')')
        point_of_interest.save()

        return HttpResponseRedirect('/neighborhood/points_of_interest/')

    return render(request, 'edit_point_of_interest.html', args)


def showPointsOfInterest(request):
    points_of_interest = None
    user_neighborhood = UserNeighborhood.objects.all().filter(user=request.user).first()
    n = Neighborhood.objects.get(pk=user_neighborhood.neighborhood.pk)
    # n = Neighborhood.objects.all().filter(user_id=request.user).first()
    if n is not None:
        points_of_interest = NeighborhoodPointOfInterest.objects.all().filter(neighborhood=n)
    return render(request, 'neighborhood_points_of_interest.html',
                  {'points': points_of_interest, 'neighborhood': n, })


def deletePointOfInterest(request, pk):
    point_of_interest = PointOfInterest.objects.get(pk=pk)

    images = PointOfInterestImage.objects.all().filter(point_of_interest=point_of_interest)
    for image in images:
        cloudinary.uploader.destroy(image.image.public_id, invalidate=True)

    point_of_interest.delete()
    return HttpResponseRedirect('/neighborhood/points_of_interest/')


def deletePointOfInterestImage(request, pk):
    image = PointOfInterestImage.objects.get(pk=pk)
    point_of_interest = image.point_of_interest
    image.delete()
    cloudinary.uploader.destroy(image.image.public_id, invalidate=True)
    images = PointOfInterestImage.objects.all().filter(point_of_interest=point_of_interest)
    return render(request,
                  'point_of_interest_images.html', {'images': images, 'point': point_of_interest, })


def uploadPointOfInterestImage(request, pk):
    args = {}
    context = dict(backend_form=PointOfInterestImageForm())
    args['context'] = context
    args['pk'] = str(pk)

    if request.method == 'POST':
        desc = request.POST.get('image-description')
        image = request.FILES['image-file']

        point_of_interest = PointOfInterest.objects.get(pk=pk)

        point_of_interest_image = PointOfInterestImage()
        point_of_interest_image.point_of_interest = point_of_interest
        point_of_interest_image.image = image
        point_of_interest_image.description = desc
        point_of_interest_image.save()

        return HttpResponseRedirect("/neighborhood/point_of_interest/" + str(pk) + "/images/")

    return render(request, 'upload_point_of_interest_image.html', args)


def editPointOfInterestImage(request, pk):
    args = {}
    image = PointOfInterestImage.objects.get(pk=pk)
    point_of_interest = image.point_of_interest
    args['image'] = image
    args['point'] = point_of_interest

    if request.method == 'POST':
        image.description = request.POST.get('image-description')
        image.save()

        return HttpResponseRedirect("/neighborhood/point_of_interest/" + str(point_of_interest.pk) + "/images/")

    return render(request, 'edit_point_of_interest_image.html', args)
