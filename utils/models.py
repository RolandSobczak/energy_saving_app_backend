from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
from datetime import datetime

class CheckAgeMixin:
    def is_older_than_n_days(self, n=1):
        """Check if created is older than now() - n days"""
        delta = timedelta(days=n)
        return datetime.now() - self.created > delta

    def created_delta(self):
        timezone.now() - self.created

class Timestamped(models.Model, CheckAgeMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super().save()
