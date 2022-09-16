from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)


def get_absolute_url(self):
    return reverse_lazy('users:users-detail', kwargs={"pk": self.id})


User.add_to_class("get_absolute_url", get_absolute_url)
