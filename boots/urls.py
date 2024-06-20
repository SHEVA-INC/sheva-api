from django.urls import path, include
from rest_framework import routers
from .views import BootsViewSet, NewBootsList, PopularBootsList, GetBootsByIdsView, \
    MainImageUpdateView, BootsUpdateView, BootsImagesUpdateView

router = routers.DefaultRouter()

router.register("", BootsViewSet)


urlpatterns = [
    path("list", include(router.urls)),
    path('new', NewBootsList.as_view(), name='new-boots'),
    path('popular', PopularBootsList.as_view(), name='popular-boots'),
    path('liked/', GetBootsByIdsView.as_view(), name='get_boots_by_ids'),
    path('boots/<int:pk>/update/', BootsUpdateView.as_view(), name='boots_update'),
    path('boots/<int:pk>/update-main-image/', MainImageUpdateView.as_view(),
         name='main_image_update'),
    path('boots/<int:pk>/update-images/', BootsImagesUpdateView.as_view(),
         name='boots_images_update'),
]

app_name = "boots"
