
"""
URL configuration for ShevaAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from ShevaAPI import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api/boots/", include("boots.urls", namespace="boots")),
    path("api/accessories/", include("accessories.urls", namespace="accessories")),
    path("api/reviews/", include("review.urls", namespace="review")),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/orders/", include("order.urls", namespace="order")),
    path("api/cart/", include("cart.urls", namespace="cart")),
    path("api/payment/", include("payment.urls", namespace="payment")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
