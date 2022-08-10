from django.shortcuts import render


def showRealTimeMap(request):
    return render(request, 'realtime_map.html')
