from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    # is the receiver function which is run every time a user is created.
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)  # post_save is the signal that is sent at the end of the save method.
def saveProfile(sender, instance, **kwargs):
    instance.profile.save()


# In general, what the above code does is after the User model's save()
# method has finished executing, it sends a signal(post_save) to the receiver function (create_profile)
# then this function will receive the signal to create and save a profile instance for that user.
