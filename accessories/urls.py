from rest_framework.routers import DefaultRouter
from django.urls import path, include
from accessories.views import AccessoriesViewSet, GetAccessoriesByIdsView

router = DefaultRouter()
router.register(r'accessories', AccessoriesViewSet, basename='accessory')

urlpatterns = [
    path('', include(router.urls)),
    path('liked-accessories/', GetAccessoriesByIdsView.as_view(), name='get_accessories_by_ids'),
]

app_name = "accessories"