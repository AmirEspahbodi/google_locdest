from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GeoViewSet

router = DefaultRouter()
router.register(r'', GeoViewSet, basename='geo')

urlpatterns = [
    path('', include(router.urls)),
]
