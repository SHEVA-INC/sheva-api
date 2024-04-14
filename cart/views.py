from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boots.models import Boots
from .models import Cart, CartProduct
from .serializers import CartSerializer, CartProductSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        product = Boots.objects.get(id=product_id)
    except Boots.DoesNotExist:
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    if CartProduct.objects.filter(cart=cart, product=product).exists():
        return Response({"message": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)

    cart_product = CartProduct.objects.create(cart=cart, product=product)
    serializer = CartProductSerializer(cart_product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
