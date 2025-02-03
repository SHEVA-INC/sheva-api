from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType

from boots.filters import CustomPageNumberPagination
from boots.models import Boots, Size
from accessories.models import Accessory
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_type = request.data.get('product_type')  # 'boots' or 'accessory'
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    size = request.data.get('size')  # Optional, only for boots

    if quantity < 1:
        return Response({"message": "Quantity must be at least 1"}, status=status.HTTP_400_BAD_REQUEST)

    cart, _ = Cart.objects.get_or_create(user=user)

    try:
        if product_type == 'boots':
            content_type = ContentType.objects.get_for_model(Boots)
            if not size:
                return Response({"message": "Size is required for boots"}, status=status.HTTP_400_BAD_REQUEST)

            product_size = Size.objects.get(boots_id=product_id, size=size)
            product = product_size.boots

            # Check if boots with this size already in cart
            if CartItem.objects.filter(
                    cart=cart,
                    content_type=content_type,
                    object_id=product.id,
                    size=size
            ).exists():
                return Response({"message": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)

        elif product_type == 'accessory':
            content_type = ContentType.objects.get_for_model(Accessory)
            product = Accessory.objects.get(id=product_id)

            if CartItem.objects.filter(
                    cart=cart,
                    content_type=content_type,
                    object_id=product.id
            ).exists():
                return Response({"message": "Product already in cart"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid product type"}, status=status.HTTP_400_BAD_REQUEST)

    except (Size.DoesNotExist, Boots.DoesNotExist, Accessory.DoesNotExist):
        return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    CartItem.objects.create(
        cart=cart,
        content_type=content_type,
        object_id=product.id,
        quantity=quantity,
        size=size if product_type == 'boots' else None
    )

    return Response({"message": "Product added to cart successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = cart.cartitems.all()
    paginator = CustomPageNumberPagination()
    page = paginator.paginate_queryset(cart_items, request)

    if page is not None:
        serializer = CartItemSerializer(page, many=True, context={'request': request})
        response_data = {
            'cart_id': cart.id,
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
            'results': serializer.data,
            'total_price': cart.total_price()
        }
        return paginator.get_paginated_response(response_data)

    serializer = CartItemSerializer(cart_items, many=True, context={'request': request})
    response_data = {
        'cart_id': cart.id,
        'results': serializer.data,
        'total_price': cart.total_price()
    }
    return Response(response_data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    user = request.user
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Product not found in cart'}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)