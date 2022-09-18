from django.db import models
from utils.models import Timestamped, SlugMixin
from utils import fields as utils_fields
from users.models import Profile


class Organisations(Timestamped, SlugMixin):
    profiles = models.ManyToManyField(Profile, related_name='organisations')
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='organisations/images/', null=True, blank=True)


class Localisation(Timestamped, SlugMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='localisations')
    organisation = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organisation_localisations')
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='localisations/images/', null=True, blank=True)


class Room(Timestamped, SlugMixin):
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='rooms/images/', null=True, blank=True)


class DeviceType(SlugMixin):
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='devices_types/images/', null=True, blank=True)


class Device(Timestamped, SlugMixin):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='devices/images/', null=True, blank=True)
    devices_types = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='devices')
    consumption = models.IntegerField()
    avg_active_time = models.IntegerField()
    localisation = models.ForeignKey(Room, on_delete=models.DO_NOTHING, related_name='devices')


class Month(Timestamped):
    date = models.DateField()
    consumption = models.IntegerField()
    description = utils_fields.HTMLField(null=True, blank=True)


class Day(Timestamped):
    date = models.DateField()
    consumption = models.IntegerField()
    description = utils_fields.HTMLField(null=True, blank=True)
