from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from user import views
from user.views import CreateUserView, UserProfileView, UserProfileUpdateView

urlpatterns = [
    path("register", CreateUserView.as_view(), name="create"),
    path("login", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("change_password", views.ChangePasswordView.as_view(), name="change_password"),
    path('profile/', UserProfileView.as_view(), name='get_profile'),
    path('profile/update', UserProfileUpdateView.as_view(), name='update_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "user"
