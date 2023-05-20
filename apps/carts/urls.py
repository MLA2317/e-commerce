from django.urls import path
from .views import cart, add_cart, add_wishlist, my_wishlist, plus_quantity, minus_quantity, delete_cart_item, checkout

app_name = 'carts'

urlpatterns = [
    path('', cart, name='cart'),
    path('add-wishlist/', add_wishlist, name='add-wishlist'),
    path('my-wishlist/', my_wishlist, name='my-wishlist'),
    path('add-cart/', add_cart, name='add-cart'),
    path('plus-quantity/', plus_quantity, name='plus_quantity'),
    path('minus-quantity/', minus_quantity, name='minus_quantity'),
    path('delete-cart-item/', delete_cart_item, name='delete_cart_item'),
    path('checkout/', checkout, name='checkout'),
]