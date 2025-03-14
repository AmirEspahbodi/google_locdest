from rest_framework import serializers


class RequestGeoAddressDistance(serializers.Serializer):
    origin = serializers.CharField(max_length=256)
    destination = serializers.CharField(max_length=256)


class ResponseGeoLocationDistance(serializers.Serializer):
    formatted_origin = serializers.CharField(max_length=256)
    formatted_destination = serializers.CharField(max_length=256)
    distance_text = serializers.CharField(max_length=256)
    distance_meters = serializers.CharField(max_length=256)