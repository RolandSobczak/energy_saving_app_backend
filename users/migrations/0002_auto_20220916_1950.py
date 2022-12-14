# Generated by Django 3.2 on 2022-09-16 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_type', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('icon', models.ImageField(upload_to='profiles/types/icons/')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='profiles', to='users.profiletype'),
            preserve_default=False,
        ),
    ]
