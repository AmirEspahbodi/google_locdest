# apps/geo/models.py

import logging
from django.db import models

# Set up a logger for this module
logger = logging.getLogger(__name__)


class Geolocation(models.Model):
    """
    Model to log geolocation requests.
    This can be used to track queries for analytics or debugging purposes.
    """

    input_address = models.CharField(max_length=255, unique=True, db_index=True)
    formatted_address = models.CharField(
        max_length=255, blank=True, null=True, unique=True, db_index=True
    )
    latitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        blank=True,
        null=True,
    )
    longitude = models.DecimalField(
        max_digits=13,
        decimal_places=10,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.input_address} -> {self.formatted_address or 'Not formatted yet'}"
        )


class GeolocationsDistance(models.Model):
    """
    Model to save the computed distance between two geolocation requests.
    """

    geolocation1 = models.ForeignKey(
        Geolocation, related_name="distance_as_first", on_delete=models.CASCADE
    )
    geolocation2 = models.ForeignKey(
        Geolocation, related_name="distance_as_second", on_delete=models.CASCADE
    )
    distance_text = models.CharField(max_length=32)
    distance_metter = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["geolocation1", "geolocation2"]),
        ]

    def __str__(self):
        return f"Distance between {self.geolocation1.id} and {self.geolocation2.id}: {self.distance_km} km"
