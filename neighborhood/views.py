import json

import cloudinary
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry

from neighborhood.forms import NeighborhoodPhotoForm
from neighborhood.models import NeighborhoodPhoto
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


def showNeighborhoodPhotos(request):
    n = Neighborhood.objects.get(user_id=request.user)
    photos = NeighborhoodPhoto.objects.all().filter(neighborhood=n)
    return render(request, 'neighborhood_photos.html', {'photos': photos, 'neighborhood': n, })


def uploadNeighborhoodPhoto(request):
    context = dict(backend_form=NeighborhoodPhotoForm())

    if request.method == 'POST':
        form = NeighborhoodPhotoForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            n = Neighborhood.objects.get(user_id=request.user)
            neighborhood_photo = NeighborhoodPhoto()
            neighborhood_photo.image = form.cleaned_data['image']
            neighborhood_photo.neighborhood = n
            neighborhood_photo.save()
            return HttpResponseRedirect('/neighborhood/photos/')

    return render(request, 'upload_neighborhood_photo.html', context)


def deleteNeighborhoodPhoto(request, pk):
    photo = NeighborhoodPhoto.objects.get(pk=pk)
    photo.delete()
    cloudinary.uploader.destroy(photo.image.public_id, invalidate=True)
    return HttpResponseRedirect('/neighborhood/photos/')


def showPointsOfInterest(request):
    return None
