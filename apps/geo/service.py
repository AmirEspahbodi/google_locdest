import logging
from random import random
from faker import Faker
logger = logging.getLogger(__name__)

async def fetch_distance_by_addresses_data(address1, address2):
    faker = Faker()
    return {
        'km': 10*random(),
        "formatted_address1": faker.address(),
        "formatted_address2": faker.address()
    }
