from django.contrib import admin
from .models import Cart, CartItem, Wishlist, Order


# Register your models here.

class CartListInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [CartListInline]


admin.site.register(Cart, CartAdmin)
admin.site.register(Wishlist)
admin.site.register(Order)

