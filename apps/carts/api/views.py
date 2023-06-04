from .serialziers import WishlistSerializer, WishlistCreateSerializer, CartSerializer, CartItemSerializer, \
    OrderSerializer
from rest_framework import generics, status, permissions, views
from ..models import Wishlist, Cart, CartItem, Order
from rest_framework.response import Response
from ...products.models import Product
from django.http import JsonResponse


class WishListListCreateAPIView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/carts/api/wishlist/list-create/
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return super().get_queryset().filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        serializer = WishlistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(user_id=user_id)


