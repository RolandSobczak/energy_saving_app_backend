from django.db import models
from utils.models import Timestamped, SlugMixin
from utils import fields as utils_fields
from users.models import Profile
import datetime


class Organisations(Timestamped, SlugMixin):
    profiles = models.ManyToManyField(Profile, related_name='organisations')
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='organisations/images/', null=True, blank=True)


class EnergyPrice(Timestamped):
    start_price = models.FloatField()
    price_after_rise = models.IntegerField()
    rise_level = models.FloatField()


class LocalisationIcon(SlugMixin):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='localisations/icons/')


class Localisation(Timestamped, SlugMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='localisations', null=True, blank=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE,
                                     related_name='organisation_localisations', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='localisations/images/', null=True, blank=True)
    energy_price = models.ForeignKey(EnergyPrice, on_delete=models.DO_NOTHING, related_name='localisations', null=True)
    icon = models.ForeignKey(LocalisationIcon, on_delete=models.DO_NOTHING, related_name='localisations', null=True)

    def get_consumption(self, start_date, end_date) -> tuple:
        results = []
        total_active_time = 0
        total_consumption = 0
        total_cost = 0
        per_day = {}
        for room in self.rooms.all():
            results.append(room.get_consumption(start_date, end_date))
        for day in results[0][1]:
            day_active_time = 0
            day_consumption = 0
            day_cost = 0
            for total in results:
                day_room_stats = total[1][day]
                day_active_time += day_room_stats['active_time']
                day_consumption += day_room_stats['consumption']
                day_cost += day_room_stats['energy_cost']
            total_active_time += day_active_time
            total_consumption += day_consumption
            total_cost += day_cost
            per_day.update({
                day: {
                    'active_time': day_active_time,
                    'consumption': day_consumption,
                    'energy_cost': day_cost,
                }
            })
        stats = {
            'total_active_time': total_active_time,
            'total_consumption': total_consumption,
            'total_cost': total_cost,
        }
        return stats, per_day


    def is_limit_exceeded(self, year: int):
        year_consumption = self.get_consumption(datetime.date(year, 1, 1), datetime.date(year, 12, 31))
        return False if year_consumption < self.energy_price.rise_level else True

    def get_real_price(self, year: int):
        return self.energy_price.start_price if self.is_limit_exceeded(year) else self.energy_price.price_after_rise

    def get_energy_cost(self, start_date, end_date):
        energy_cost_sum = 0
        for room in self.rooms.all():
            energy_cost_sum += room.get_energy_cost(start_date, end_date)
        return energy_cost_sum

    def get_offers(self) -> tuple:
        offers = []
        for room in self.rooms.all():
            offer = room.get_offers()
            offers += offer
        return tuple(offers)


class RoomIcon(SlugMixin):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='rooms/icons/')


class Room(Timestamped, SlugMixin):
    localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='rooms/images/', null=True, blank=True)
    icon = models.ForeignKey(RoomIcon, on_delete=models.DO_NOTHING, related_name='rooms', null=True)

    def get_consumption(self, start_date, end_date):
        results = []
        total_active_time = 0
        total_consumption = 0
        total_cost = 0
        per_day = {}
        for device in self.devices.all():
            results.append(device.get_energy_cost(start_date, end_date))
        for day in results[0][1]:
            day_active_time = 0
            day_consumption = 0
            day_cost = 0
            for total in results:
                day_device_stats = total[1][day]
                day_active_time += day_device_stats['active_time']
                day_consumption += day_device_stats['consumption']
                day_cost += day_device_stats['energy_cost']
            total_active_time += day_active_time
            total_consumption += day_consumption
            total_cost += day_cost
            per_day.update({
                day: {
                    'active_time': day_active_time,
                    'consumption': day_consumption,
                    'energy_cost': day_cost,
                }
            })
        stats = {
            'total_active_time': total_active_time,
            'total_consumption': total_consumption,
            'total_cost': total_cost,
        }
        return stats, per_day

    def get_offers(self) -> tuple:
        offers = []
        for device in self.devices.all():
            offer = device.get_offer()
            if offer is not None:
                offers.append(offer)
        return tuple(offers)


class GroupIcon(SlugMixin):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='groups/icons/')


class Group(SlugMixin):
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='groups/images/', null=True, blank=True)
    icon = models.ForeignKey(GroupIcon, on_delete=models.DO_NOTHING, related_name='groups', null=True)

    def get_consumption(self, start_date, end_date):
        results = []
        total_active_time = 0
        total_consumption = 0
        total_cost = 0
        per_day = {}
        for device in self.devices.all():
            results.append(device.get_energy_cost(start_date, end_date))
        for day in results[0][1]:
            day_active_time = 0
            day_consumption = 0
            day_cost = 0
            for total in results:
                day_device_stats = total[1][day]
                day_active_time += day_device_stats['active_time']
                day_consumption += day_device_stats['consumption']
                day_cost += day_device_stats['energy_cost']
            total_active_time += day_active_time
            total_consumption += day_consumption
            total_cost += day_cost
            per_day.update({
                day: {
                    'active_time': day_active_time,
                    'consumption': day_consumption,
                    'energy_cost': day_cost,
                }
            })
        stats = {
            'total_active_time': total_active_time,
            'total_consumption': total_consumption,
            'total_cost': total_cost,
        }
        return stats, per_day

    def get_offers(self) -> tuple:
        offers = []
        for device in self.devices.all():
            offer = device.get_offer()
            if offer is not None:
                offers.append(offer)
        return tuple(offers)


class DeviceType(SlugMixin):
    name = models.CharField(max_length=255)
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='devices_types/images/', null=True, blank=True)


class ProductOffer(SlugMixin):
    device_type = models.OneToOneField(DeviceType, on_delete=models.CASCADE, related_name='offer')
    name = models.CharField(max_length=255)
    consumption = models.IntegerField()
    url = models.URLField()
    image_url = models.URLField()
    price = models.FloatField()


class WeekDay(SlugMixin):
    name = models.CharField(max_length=255)
    index = models.IntegerField()


class Device(Timestamped, SlugMixin):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    active_days = models.ManyToManyField(WeekDay, related_name='devices')
    description = utils_fields.HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to='devices/images/', null=True, blank=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, related_name='devices')
    consumption = models.IntegerField()
    avg_active_time = models.IntegerField()
    localisation = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='devices', null=True, blank=True)
    energy_class = models.CharField(max_length=255)

    def get_active_time(self, start_date, end_date) -> tuple:
        days_counter = (end_date - start_date).days
        active_time_sum = 0
        active_time_per_day = {}
        active_days = [day.index for day in self.active_days.all()]
        print(active_days)
        months = Month.objects.prefetch_related('days').filter(date__gte=start_date, date__lte=end_date, device=self)
        for counter in range(days_counter + 1):
            date = start_date + datetime.timedelta(counter)
            is_active_date = date.isoweekday() in active_days
            month = tuple(filter(lambda month_obj: month_obj.date == datetime.date(date.year, date.month, 1), months))
            active_time = self.avg_active_time if is_active_date else 0
            if month:
                day = tuple(filter(lambda day: day.date == date, month[0].days.all()))
                active_time = month[0].avg_active_time if is_active_date else 0
                if day:
                    active_time = day[0].active_time
            active_time_sum += active_time
            active_time_per_day.update({date.isoformat(): active_time})
        return active_time_sum, active_time_per_day

    def get_consumption(self, start_date, end_date) -> tuple:
        active_time = self.get_active_time(start_date, end_date)
        consumption_sum = active_time[0] * self.consumption
        consumption_per_day = {}
        for key, value in active_time[1].items():
            consumption_per_day.update({
                key: {
                    'active_time': value,
                    'consumption': value * self.consumption
                }
            })
        total = {
            'total_consumption': consumption_sum,
            'total_active_time': active_time[0],
        }
        return total, consumption_per_day

    def get_energy_cost(self, start_date, end_date) -> tuple:
        localisation = self.localisation.localisation
        energy_price = localisation.energy_price.start_price
        consumption = self.get_consumption(start_date, end_date)
        total_energy_cost = consumption[0]['total_consumption'] / 1000 * energy_price
        energy_cost_per_day = {}
        for key, value in consumption[1].items():
            energy_cost_per_day.update({
                key: {
                    'active_time': value['active_time'],
                    'consumption': value['consumption'],
                    'energy_cost': value['consumption'] / 1000 * energy_price,
                }
            })
        total = {
            'total_consumption': consumption[0]['total_consumption'],
            'total_active_time': consumption[0]['total_active_time'],
            'total_energy_cost': total_energy_cost,
        }
        return total, energy_cost_per_day

    def get_offer(self):
        proposition = self.device_type.offer
        if proposition.consumption < self.consumption:
            stats_last_month = self.get_energy_cost(
                datetime.date.today() - datetime.datetime(31),
                datetime.date.today()
            )
            energy_cost = stats_last_month[0]['total_energy_cost']
            active_time = stats_last_month[0]['total_active_time']
            energy_price = self.localisation.localisation.energy_price.start_price
            offer_month_cost = proposition.consumption * active_time / 1000 * energy_price
            one_month_profit = energy_cost - offer_month_cost
            reimbursement_after = int(proposition.price / one_month_profit)
            return {
                'name': proposition.name,
                'consumption': proposition.consumption,
                'url': proposition.url,
                'image_url': proposition.image_url,
                'price': proposition.price,
                'reimbursement_after': reimbursement_after,
                'actual_device': self.id,
            }
        return None


class Month(Timestamped):
    class Meta:
        unique_together = ['date', 'device']

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='months')
    date = models.DateField()
    avg_active_time = models.IntegerField()
    description = utils_fields.HTMLField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.date = datetime.date(self.date.year, self.date.month, 1)
        super().save()


class Day(Timestamped):
    class Meta:
        unique_together = ['date', 'month']

    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='days')
    date = models.DateField()
    active_time = models.IntegerField()
    description = utils_fields.HTMLField(null=True, blank=True)
