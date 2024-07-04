from django.urls import path
from cart.views import get_cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('view_cart', get_cart, name='user-cart'),
    path('add-to-cart/<int:product_id>/<int:quantity>/<int:size>/', add_to_cart, name='add-to-cart'),
    path('cart/remove-from-cart/<int:cart_product_id>/', remove_from_cart, name='remove_from_cart'),
]


app_name = "cart"
