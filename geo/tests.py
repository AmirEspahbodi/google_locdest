# geo/tests.py

import pytest
from django.test import AsyncClient
from geo import service
from faker import Faker

@pytest.mark.django_db
@pytest.mark.asyncio
async def test_geocode_endpoint():
    """
    Test the geocode endpoint using an asynchronous test client.
    We simulate an external API call by monkeypatching the fetch_geocode_data
    function to return a fake response.
    """
    
    
    faker = Faker()
    addresses = [
        '100 John F Shelley Dr, San Francisco, CA 94134, United States',
        '1100 Veterans Blvd, Redwood City, CA 94063, United States',
        faker.address(),
        '1701 Airport Blvd Ste B-1130, San Jose, CA 95110, United States',
        '2200 Front St, Sacramento, CA 95818, United States',
        faker.address(),
        faker.address(),
        '37 Old Courthouse Sq, Santa Rosa, CA 95404, United States',
        faker.address(),
        '1201 N Pershing Ave, Stockton, CA 95203, United States',
        '1402 I St, Modesto, CA 95354, United States',
        faker.address(),
        faker.address(),
        '669 F St, Williams, CA 95987, United States',
        '11101 Lansing St, Mendocino, CA 95460, United States',
        '1945 N St, Newman, CA 95360, United States',
        '15290 Lakeshore Dr, Clearlake, CA 95422, United States',
        '9435 Konocti Bay Rd, Kelseyville, CA 95451, United States',
        faker.address(),
        faker.address(),
        '669 F St, Williams, CA 95987, United States',
        '11101 Lansing St, Mendocino, CA 95460, United States',
    ]
    
    for i in range(len(addresses)):
        for j in range(i+1, len(addresses)):
            origin = addresses[i]
            destination = addresses[j]
            
            client = AsyncClient()
            url = "/api/geo/geoaddress/"
            payload = {
                "origin": origin,
                "destination": destination,
            }
            
            response = await client.post(url, data=payload)
            respone_data = response.json()
            print(respone_data)
            print(type(respone_data))
            
            if response.status_code == 500:
                assert respone_data['error']=="Failed to fetch geocode data."
                
            if response.status_code == 400:
                print(response)
                assert respone_data['error']=="Invalid input data."
                
            if response.status_code == 200:
                assert respone_data.get("formatted_origin", None) != None
                assert respone_data.get("origin_latitude", None) != None
                assert respone_data.get("origin_longitude", None) != None
                assert respone_data.get("formatted_destination", None) != None
                assert respone_data.get("destination_latitude", None) != None
                assert respone_data.get("destination_longitude", None) != None
                assert respone_data.get("distance_text", None) != None
                assert respone_data.get("distance_meters", None) != None
