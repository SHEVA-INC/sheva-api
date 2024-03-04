from rest_framework import routers
from .views import ReviewViewSet

router = routers.DefaultRouter()

router.register("", ReviewViewSet)


urlpatterns = router.urls

app_name = "review"
