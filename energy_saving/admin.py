from django.contrib import admin
from . import models

@admin.register(models.Organisations)
class OrganisationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EnergyPrice)
class EnergyPriceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LocalisationIcon)
class LocalisationIconAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Localisation)
class LocalisationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.RoomIcon)
class RoomIconAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(models.GroupIcon)
class GroupIconAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Month)
class MonthAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Day)
class DayAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    pass


@admin.register(models.WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    pass
