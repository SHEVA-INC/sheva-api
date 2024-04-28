from django.urls import path, include
from rest_framework import routers
from .views import BootsViewSet, NewBootsList, PopularBootsList

router = routers.DefaultRouter()

router.register("", BootsViewSet)


urlpatterns = [
    path("list/", include(router.urls)),
    path('new/', NewBootsList.as_view(), name='new-boots'),
    path('popular/', PopularBootsList.as_view(), name='popular-boots'),
]

app_name = "boots"
