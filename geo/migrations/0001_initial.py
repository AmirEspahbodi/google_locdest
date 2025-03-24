# Generated by Django 5.1.7 on 2025-03-14 11:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_address', models.CharField(max_length=255)),
                ('formatted_address', models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=10, max_digits=13, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=10, max_digits=13, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeolocationsDistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance_text', models.FloatField()),
                ('distance_metter', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('geolocation1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distance_as_first', to='geo.geolocation')),
                ('geolocation2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distance_as_second', to='geo.geolocation')),
            ],
            options={
                'indexes': [models.Index(fields=['geolocation1', 'geolocation2'], name='geo_geoloca_geoloca_559d90_idx')],
            },
        ),
    ]
