from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse_lazy


User = get_user_model()


class ProfileType(models.Model):
    profile_type = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    icon = models.ImageField(upload_to='profiles/types/icons/', null=True, blank=True)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.profile_type)
        super().save()

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='users/images/', null=True, blank=True)
    type = models.ForeignKey(ProfileType, on_delete=models.DO_NOTHING, related_name='profiles')


