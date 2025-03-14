import logging
import httpx
from httpx import Response
import asyncio
from random import random
from django.conf import settings

logger = logging.getLogger(__name__)
        

async def format_addresses(addresses):
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
    
    formatted_addresses = []
    
    async with httpx.AsyncClient() as alient:
        responses_coroutine = []
        for address in addresses:
            # Call the Geocoding API
            endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "address": address,
                "key": api_key
            }
            responses_coroutine.append(alient.get(endpoint, params=params))
        responses:list[Response] = await asyncio.gather(*responses_coroutine)

    for response in responses:
        data = response.json()
        if data["status"] == "OK":
            # Get the formatted address from the first result
            formatted_address = data["results"][0]["formatted_address"]
            formatted_addresses.append(formatted_address)
        else:
            formatted_addresses.append(f"Error: {data['status']}")
    
    return formatted_addresses

async def fetch_distance_by_addresses_data(address1, address2):
    formatted_address1, formatted_address2 = await format_addresses([address1, address2])
    return {
        'km': 10*random(),
        "formatted_address1": formatted_address1,
        "formatted_address2": formatted_address2
    }

"5555 E Washington Blvd, Commerce, CA 90040, United States"
"US-95, Las Vegas, NV 89104, USA"