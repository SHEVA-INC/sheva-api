from django.urls import path
from cart.views import view_cart, add_to_cart

urlpatterns = [
    path('view_cart/', view_cart, name='user-cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
]


app_name = "cart"
