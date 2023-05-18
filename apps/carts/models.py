import uuid
from django.contrib.auth.models import User
from django.db import models
from apps.products.models import Product


# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'wishlist of {self.user.username} (id: {self.id})'


class Cart(models.Model):
    clients = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_ordered = models.BooleanField(default=False)

    @property
    def get_cart_items(self):
        cart_items = self.cart_items.all()
        total = sum([item.quantity for item in cart_items])
        return total

    @property
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        total = sum([item.get_item_total for item in cart_items])
        return total

    def __str__(self):
        return f'cart of {self.clients} (id: {self.id})'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def get_item_total(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS = (
        (0, 'NEW'),
        (1, 'PROCESS'),
        (2, 'DELIVERED'),
        (3, 'CANCELLED'),
    )
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=21)
    address = models.CharField(max_length=255)
    note = models.CharField(null=True, blank=True, max_length=255)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order of {self.client} (id: {self.id}) | {self.transaction_id}'
