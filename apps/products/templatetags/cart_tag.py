from django import template
from apps.carts.models import *
from apps.products.models import Category

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_cart(context):
    request = context['request']
    user = request.user
    try:
        cart = Cart.objects.get(client=user, is_ordered=False)
    except:
        cart = []
    return cart


@register.simple_tag(takes_context=True)
def get_user_wishlist(context):
    request = context['request']
    user = request.user
    try:
        wl = Wishlist.objects.filter(user=user)
    except:
        wl = []
    wlist_products = [product.product.id for product in wl]
    return wlist_products


@register.simple_tag()
def categories():
    try:
        cat = Category.objects.all()
    except:
        cat = None
    return cat
