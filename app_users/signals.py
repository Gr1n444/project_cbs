from django.db.models.signals import post_save
from app_users.models import Profile


def updateProfile(instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.first_name
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(updateProfile, sender=Profile)