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

    input_address = models.CharField(max_length=255)
    formatted_address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, db_index=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        logger.info("Saving GeolocationRequest for address: %s", self.input_address)
        super().save(*args, **kwargs)

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
    distance_km = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["geolocation1", "geolocation2"]),
        ]

    def __str__(self):
        return f"Distance between {self.geolocation1.id} and {self.geolocation2.id}: {self.distance_km} km"
