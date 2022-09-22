from rest_framework import serializers
from . import models


class OrganisationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organisations
        fields = ('pk', 'profiles', 'name', 'description', 'image',)


class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Localisation
        fields = ('pk', 'profile', 'organisations', 'name', 'description', 'image',)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ('pk', 'localisation', 'name', 'description', 'image',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Group
        fields = '__all__'


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceType
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Device
        fields = ('pk', 'name', 'active', 'description', 'image', 'device_type',
                  'consumption', 'avg_active_time', 'localisation',)


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Month
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = '__all__'


