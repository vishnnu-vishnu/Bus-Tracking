# Generated by Django 5.0.1 on 2024-03-01 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApi', '0002_bus_place_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='places',
        ),
        migrations.RemoveField(
            model_name='route',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Place',
        ),
        migrations.DeleteModel(
            name='Route',
        ),
    ]