from django.urls import path

from realtime_map.views import showRealTimeMap

app_name = 'realtime_map'

urlpatterns = [
    path('realtime_map/', showRealTimeMap, name='showRealTimeMap'),
]
