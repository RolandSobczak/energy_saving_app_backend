from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)


class ProfileType(models.Model):
    profile_type = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='profiles/types/icons/')