# Generated by Django 4.2.5 on 2024-03-02 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApi', '0013_alter_busdriver_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='routeassign',
            name='busowner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AdminApi.busowner'),
        ),
    ]