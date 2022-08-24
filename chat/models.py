from django.db import models
from django.contrib.auth.models import User
from registration.models import Neighborhood

class NeighborhoodChat(models.Model):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    def __str__(self):
        return self.neighborhood.name + ' chat'

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(NeighborhoodChat, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=True)
    time = models.DateTimeField(auto_now_add=True)
