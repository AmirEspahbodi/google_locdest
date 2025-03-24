# apps/geo/views.py

import logging
from asgiref.sync import async_to_sync
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from .serializers import RequestGeoAddressDistance, ResponseGeoLocationDistance
from .service import fetch_distance_by_addresses_data
from .models import Geolocation, GeolocationsDistance

logger = logging.getLogger(__name__)


@extend_schema_view(
    geoaddressdistance=extend_schema(
        summary="get geometric distance between two given address in km",
        description="get geometric distance between two given address in km.",
        request=RequestGeoAddressDistance,
        responses={
            200: OpenApiResponse(
                response=ResponseGeoLocationDistance,
                description="geoaddress data response in km",
            )
        },
    )
)
class GeoViewSet(viewsets.ViewSet):
    @staticmethod
    def get_from_db(
        origin, destination, origin_obj=None, destination_obj=None, geolocations_distance_obj=None
    ):
        
        if origin_obj is None:
            try:
                origin_obj = Geolocation.objects.get(input_address=origin)
                logger.info(f"get origin_obj")
            except BaseException as e:
                origin_obj = None
                logger.warning(f"could not get origin objects from db catched exception is, catched exception is: {e}")
        if destination_obj is None:
            try:
                destination_obj = Geolocation.objects.get(input_address=destination)
                logger.info(f"get destination_obj")
            except BaseException as e:
                destination_obj = None
                logger.warning(f"could not get destination objects from db by given input, catched exception is: {e}")

        if origin_obj is not None and destination_obj is not None:
            try:
                geolocations_distance_obj = GeolocationsDistance.objects.get(
                    Q(
                        geolocation1=origin_obj,
                        geolocation2=destination_obj,
                    )
                    | Q(
                        geolocation1=destination_obj,
                        geolocation2=origin_obj,
                    )
                )
                logger.info(f"get geolocations_distance_obj")
            except BaseException as e:
                logger.warning(f"could not get GeolocationsDistance objects from db by given input catched exception is: {e}")
                geolocations_distance_obj = None
        
        return origin_obj, destination_obj, geolocations_distance_obj 
    
    
    @action(detail=False, methods=["post"], url_path="geoaddress")
    def geoaddressdistance(self, request):
        serializer = RequestGeoAddressDistance(data=request.data)
        if serializer.is_valid():
            origin = serializer.validated_data["origin"].strip()
            destination = serializer.validated_data["destination"].strip()
            
            origin_obj, destination_obj, geolocations_distance_obj = self.get_from_db(origin, destination)

            if geolocations_distance_obj:
                return Response(
                    data={
                        "formatted_origin": origin_obj.formatted_address, 
                        "origin_latitude": origin_obj.latitude, 
                        "origin_longitude": origin_obj.longitude, 
                        "formatted_destination": destination_obj.formatted_address, 
                        "destination_latitude": destination_obj.latitude, 
                        "destination_longitude": destination_obj.longitude, 
                        "distance_text": geolocations_distance_obj.distance_text, 
                        "distance_meters": geolocations_distance_obj.distance_metter
                    }
                )

            logger.info("got two valid address")
            try:
                data = async_to_sync(fetch_distance_by_addresses_data)(
                    origin, destination
                )
            except Exception as e:
                logger.exception(f"Failed to fetch geocode data. catched exception is {e}")
                return Response(
                    {"error": "Failed to fetch geocode data.", "detail": "Failed to fetch geocode data."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response_serializer = ResponseGeoLocationDistance(data=data)
            response_serializer.is_valid(raise_exception=True)
            validated_data = response_serializer.validated_data

            origin_obj, destination_obj, geolocations_distance_obj = self.get_from_db(validated_data["formatted_origin"], validated_data["formatted_destination"], origin_obj, destination_obj, geolocations_distance_obj)

            try:
                if origin_obj is None:
                    origin_obj = Geolocation(
                        input_address=origin,
                        formatted_address=validated_data["formatted_origin"],
                        latitude=validated_data["origin_latitude"],
                        longitude=validated_data["origin_longitude"],
                    )
                    origin_obj.save()
                if destination_obj is None:
                    destination_obj = Geolocation(
                        input_address=destination,
                        formatted_address=validated_data["formatted_destination"],
                        latitude=validated_data["destination_latitude"],
                        longitude=validated_data["destination_longitude"],
                    )
                    destination_obj.save()
                if origin_obj is None and destination_obj is None:
                    geolocations_distance = GeolocationsDistance(
                        geolocation1=origin_obj,
                        geolocation2=destination_obj,
                        distance_text=validated_data["distance_text"],
                        distance_metter=validated_data["distance_meters"],
                    ).save()
            except BaseException as e:
                logger.warning(f"catched exception is: {e}")

            return Response(response_serializer.data)
        else:
            logger.info("got a invalid address")
        logger.warning("we got Invalid data from user: %s", serializer.errors)
        return Response({"error": "Invalid input data", "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
