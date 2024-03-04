from django.urls import path, include
from rest_framework import routers
from .views import BootsViewSet

router = routers.DefaultRouter()

router.register("", BootsViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "boots"
