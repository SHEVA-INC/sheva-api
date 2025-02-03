from django.urls import path
from cart.views import get_cart, add_to_cart, remove_from_cart

urlpatterns = [
    path('', get_cart, name='get_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
]


app_name = "cart"
