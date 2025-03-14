# apps/geo/views.py

import logging
from asgiref.sync import async_to_sync

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import RequestGeoAddressDistance, ResponseGeoLocationDistance
from .service import fetch_distance_by_addresses_data
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse


logger = logging.getLogger(__name__)


@extend_schema_view(
    geoaddressdistance=extend_schema(
        summary="get geometric distance between two given address in km",
        description="get geometric distance between two given address in km.",
        request=RequestGeoAddressDistance,
        responses={200: OpenApiResponse(response=ResponseGeoLocationDistance, description="geoaddress data response in km")},
    )
)
class GeoViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["post"], url_path="geoaddress")
    def geoaddressdistance(self, request):
        serializer = RequestGeoAddressDistance(data=request.data)
        if serializer.is_valid():
            address1 = serializer.validated_data["address1"]
            address2 = serializer.validated_data["address2"]
            logger.info("got two valid address")
            try:
                data = async_to_sync(fetch_distance_by_addresses_data)(address1, address2)
                return Response(data, status=status.HTTP_200_OK)
            except Exception:
                logger.exception("Failed to fetch geocode data.")
                return Response({"error": "Failed to fetch geocode data."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.info("got a invalid address")
        logger.error("Invalid data: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
