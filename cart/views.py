from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from boots.filters import CustomPageNumberPagination
from boots.models import Boots, Size
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

    cart_products = cart.cartproduct_set.all()

    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(cart_products, request)
    if page is not None:
        serializer = CartProductSerializer(page, many=True, context={'request': request})
        response_data = {
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
            'results': serializer.data
        }
        return paginator.get_paginated_response(response_data['results'])

    serializer = CartProductSerializer(cart_products, many=True, context={'request': request})
    response_data = {
        'results': serializer.data
    }
    return Response(response_data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request, product_id, quantity, size):
    user = request.user

    if quantity < 1:
        return Response({"message": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)

    cart, created = Cart.objects.get_or_create(user=user)

    try:
        product_size = Size.objects.get(boots_id=product_id, size=size)
        product = product_size.boots
    except Size.DoesNotExist:
        return Response({"message": "Product with this size not found"}, status=status.HTTP_404_NOT_FOUND)

    if CartProduct.objects.filter(cart=cart, product=product, size=size).exists():
        return Response({"message": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)

    cart_product = CartProduct.objects.create(cart=cart, product=product, size=size, quantity=quantity)
    serializer = CartProductSerializer(cart_product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)