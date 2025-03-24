# Distance Calculator API

## Project Overview

The Google LocDest Project is a full-stack application that provides geolocation services through a Django REST API. The backend integrates with the Google Maps API to perform forward and reverse geocoding and to calculate the distance between two geographical locations. It is built using Django, Django REST Framework, and asynchronous HTTP requests with httpx, ensuring that multiple external requests can be handled in parallel. The project also features interactive API documentation using drf-spectacular and is fully containerized with Docker and Docker Compose for easy deployment.


### Features
- **RESTful API:** Built with Django REST Framework.
- **Asynchronous Operations:** Uses async functions with httpx for external API calls and `sync_to_async` for Django ORM operations.
- **Google Maps API Integration:** Fetches geolocation data (forward and reverse geocoding) and calculates distances.
- **Interactive API Documentation:** Uses drf-spectacular for Swagger UI and Redoc.
- **Environment Management:** Uses django-environ to manage environment variables.
- **CORS Enabled:** Configured to allow requests from the React front end.
- **Containerized Deployment:** Multi-stage Dockerfile and Docker Compose for a production-ready environment.
- **Database:** Uses PostgreSQL as the database backend.

### Packages Installed
- **Django** – Web framework.
- **Django REST Framework** – For building robust REST APIs.
- **drf-spectacular** – For auto-generating OpenAPI documentation (Swagger UI & Redoc).
- **django-environ** – To manage environment variables.
- **django-cors-headers** – To handle CORS for cross-origin requests.
- **httpx** – For asynchronous HTTP requests.
- **psycopg2-binary** – PostgreSQL adapter.
- **uvicorn** – ASGI server for asynchronous support.
- **poetry** – Dependency management and packaging.

## Technology Stack

### Backend
- **Django 4.2.x**: Core framework
- **Django REST Framework**: API development
- **ASGI**: Asynchronous server gateway interface
- **Gunicorn with Uvicorn**: High-performance async server
- **PostgreSQL**: Database
- **Poetry**: Package management

### DevOps
- **Docker & Docker Compose**: Containerization
- **Multi-staged Dockerfile**: Optimized container builds
- **Environment Variables**: Using django-environ

### Documentation
- **DRF Spectacular**: API documentation (Swagger/ReDoc)

## Project Structure

```
.
├── django_config
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── uvicorn_worker.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── geo
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── service.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Google Maps API Key

### Environment Variables
The project uses django-environ for environment variable management. Create a `.env` file in the root directory with the following variables:

```
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
POSTGRES_DB=distance_calculator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgres://postgres:postgres@db:5432/distance_calculator

# Google Maps API
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
```

### Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

2. Apply migrations:
```bash
docker-compose exec web poetry run python manage.py migrate
```

3. Create a superuser (optional):
```bash
docker-compose exec web poetry run python manage.py createsuperuser
```

4. Access the API at http://localhost:8000/api/

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## Asynchronous Processing

The application leverages Django's asynchronous capabilities through ASGI and Uvicorn. This allows for parallel processing of multiple Google Maps API requests, significantly improving performance.

The server is configured to run with:
```
gunicorn django_config.asgi:application --workers 4 --threads 8 --worker-class django_config.uvicorn_worker.CustomWorker --bind 0.0.0.0:8000
```

## CORS and Security

CORS is enabled via django-cors-headers to allow requests from the React front end running at http://localhost:5173. Allowed hosts are configured in the settings (and via environment variables) to ensure that only specified domains can access the API. In production, you should specify allowed origins in the `.env` file: 

```
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

The `ALLOWED_HOSTS` setting restricts which hosts the Django site can serve. By default, it's set to `localhost` and `127.0.0.1` for development.

## API Endpoints

### Geocoding

- `POST /api/geocode/`: Convert a free-text address to formatted address with coordinates
- `POST /api/reverse-geocode/`: Convert coordinates to a formatted address

### Distance Calculation

- `POST /api/calculate-distance/`: Calculate the distance between two locations

## Docker Optimization

The Dockerfile is multi-staged to optimize the build process and reduce the final image size:
1. First stage installs dependencies and sets up the environment
2. Second stage copies only the necessary files for production

## Database

The project uses PostgreSQL as the database backend. The database schema is optimized for:
- Efficient querying of location data
- Proper indexing for high-performance retrieval
- Scalability for handling millions of records

## Integrations

### Google Maps API

The application uses the following Google Maps API endpoints:
- Geocoding API: Converts addresses to coordinates
- Reverse Geocoding API: Converts coordinates to addresses

## Testing

Run tests with:
```bash
sudo docker compose exec web poetry run pytest
```

## License

This project is licensed under the MIT License.