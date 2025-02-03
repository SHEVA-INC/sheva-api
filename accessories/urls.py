from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accessories.views import AccessoriesViewSet

router = DefaultRouter()
router.register(r'accessories', AccessoriesViewSet, basename='accessory')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "accessories"