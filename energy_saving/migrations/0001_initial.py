# Generated by Django 3.2 on 2022-09-18 15:07

from django.db import migrations, models
import django.db.models.deletion
import utils.fields
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20220916_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('consumption', models.IntegerField()),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='devices_types/images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='localisations/images/')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organisation_localisations', to='users.profile')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localisations', to='users.profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('consumption', models.IntegerField()),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='rooms/images/')),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='energy_saving.localisation')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
        migrations.CreateModel(
            name='Organisations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='organisations/images/')),
                ('profiles', models.ManyToManyField(related_name='organisations', to='users.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('description', utils.fields.HTMLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='devices/images/')),
                ('consumption', models.IntegerField()),
                ('avg_active_time', models.IntegerField()),
                ('devices_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='energy_saving.devicetype')),
                ('localisation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='devices', to='energy_saving.room')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, utils.models.CheckAgeMixin),
        ),
    ]
