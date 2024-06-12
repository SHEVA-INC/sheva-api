from django.urls import path
from cart.views import get_cart, add_to_cart

urlpatterns = [
    path('view_cart', get_cart, name='user-cart'),
    path('add-to-cart/<int:product_id>/<int:quantity>/<int:size>/', add_to_cart, name='add-to-cart'),
]


app_name = "cart"
