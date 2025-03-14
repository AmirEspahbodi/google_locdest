import logging
import httpx
from httpx import Response
import asyncio
from random import random
from django.conf import settings


logger = logging.getLogger(__name__)


async def get_data_from_google_map(origin, destination):
    """
    Format addresses using Google Maps Geocoding API

    Args:
        addresses (list): List of address strings

    Returns:
        list: List of formatted addresses
    """
    # You should set your API key as an environment variable
    api_key = settings.GOOGLE_MAP_API_KEY
    if not api_key:
        raise ValueError("Google Maps API key not found in environment variables")

    async with httpx.AsyncClient() as alient:
        responses_coroutine = []
        # Call the Geocoding API
        endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

        responses_coroutine.extend(
            [
                alient.get(endpoint, params={"address": origin, "key": api_key}),
                alient.get(endpoint, params={"address": destination, "key": api_key}),
                alient.get(
                    "https://maps.googleapis.com/maps/api/directions/json",
                    params={
                        "origin": origin,
                        "destination": destination,
                        "alternatives": "true",
                        "key": api_key,
                    },
                ),
            ]
        )

        responses: list[Response] = await asyncio.gather(*responses_coroutine)

    result = []
    # get properly formatted addressi
    for response in responses[:2]:
        data = response.json()
        if data["status"] == "OK":
            # Get the formatted address from the first result
            formatted_address = data["results"][0]["formatted_address"]
            result.append(formatted_address)
        else:
            result.append(f"Error: {data['status']}")

    # get
    distance_response = responses[2]
    if distance_response.status_code != 200:
        raise Exception(
            f"Distance Matrix request failed with status {distance_response.status_code} {distance_response.json()}"
        )

    distance_data = distance_response.json()
    if distance_data.get("status") == "OK":
        shortest_route = min(distance_data["routes"], key=lambda route: route["legs"][0]["distance"]["value"])
        result.append(shortest_route["legs"][0]["distance"]["text"])
        result.append(shortest_route["legs"][0]["distance"]["value"])
    
    else:
        print(distance_data)
        raise Exception(f"Distance Matrix error: {distance_data.get('status')}")

    return result


async def fetch_distance_by_addresses_data(origin, destination):
    formatted_origin, formatted_destination, distance_text, distance_meters = await get_data_from_google_map(
        origin, destination
    )
    return {
        "formatted_origin": formatted_origin,
        "formatted_destination": formatted_destination,
        "distance_text": distance_text,
        "distance_meters": distance_meters
    }
