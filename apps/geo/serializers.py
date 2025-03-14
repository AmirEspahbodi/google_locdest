from rest_framework import serializers


class RequestGeoAddressDistance(serializers.Serializer):
    address1 = serializers.CharField(max_length=64)
    address2 = serializers.CharField(max_length=64)


class RequestGeoCoordinateDistance(serializers.Serializer):
    latitude1 = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude1 = serializers.DecimalField(max_digits=9, decimal_places=6)

    latitude2 = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude2 = serializers.DecimalField(max_digits=9, decimal_places=6)


class ResponseGeoLocationDistance(serializers.Serializer):
    km = serializers.FloatField()
