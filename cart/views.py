from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boots.models import Boots
from .models import Cart, CartProduct
from .serializers import CartSerializer, CartProductSerializer


@api_view(['GET'])
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        product = Boots.objects.get(id=product_id)
    except Boots.DoesNotExist:
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    cart_product = CartProduct.objects.create(cart=cart, product=product)

    serializer = CartProductSerializer(cart_product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
