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

    def perform_create(self, serializer): # serializerni parametr sifatida qabul qilib, serializer orqali kiritilyotgan malumotlarni saqlashga imkon beradi
        user_id = self.request.user.id
        serializer.save(user_id=user_id)


class AddToCartCreateApi(views.APIView):
    queryset = Cart.objects.all()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        pid = request.data.get('_pid')
        user = request.user
        product = Product.objects.filter(id=pid).first()
        my_cart, new_cart = Cart.objects.get_or_create(clients=user, is_ordered=False)
        data = None
        if product:
            if my_cart:
                CartItem.objects.create(product=product, cart=my_cart)
                data = {
                    'success': True,
                    'product': product.name
                }
            if new_cart:
                CartItem.objects.create(product=product, cart=new_cart)
                data = {
                    'success': True,
                    'product': product.name
                }
            return Response(data, status=status.HTTP_201_CREATED)

        else:
            return Response({'success': False, 'message': "Mahsulot to'pilmadi"}, status=status.HTTP_404_NOT_FOUND)


class MyCartListApi(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        qs = super().get_queryset().filter(clients=self.request.user, is_ordered=False)
        return qs


class DeleteFromMyCart(generics.RetrieveDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cart_id = request.data.get('cart_id')
        cart = Cart.objects.filter(id=cart_id).first()
        serializer.is_valid(raise_exception=True)
        serializer.save(client_id=request.user.id, cart_id=cart.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





