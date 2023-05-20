from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order, Cart, CartItem, Wishlist
from apps.products.models import Product


@login_required
def cart(request):
    car, car = Cart.objects.get_or_create(client=request.user, is_ordered=False)
    ctx = {
        'cart': car
    }
    return render(request, 'shop/shoping-cart.html', ctx)


def add_wishlist(request):
    pid = request.GET.get('_pid')
    product = Product.objects.get(id=pid)
    count = Wishlist.objects.filter(user=request.user, product=product).count()
    if count < 1:
        Wishlist.objects.create(user=request.user, product=product)
        data = {
            'success': True,
            'product': product.name,
            'message': 'successfully added your wishlist'
        }
    else:
        Wishlist.objects.get(user=request.user, product=product).delete()
        data = {
            'success': False,
            'product': product.name,
            'message': 'successfully removed from your wishlist'
        }
    return JsonResponse(data)


@login_required
def my_wishlist(request):
    my_wish = Wishlist.objects.filter(user=request.user)
    latest_products = Product.objects.order_by('-id')[:6]
    ctx = {
        'products': my_wish,
        'latest_products': latest_products
    }
    return render(request, 'shop/mywishlist.html', ctx)


def add_cart(request):
    pid = request.GET.get('_pid')
    user = request.user
    product = Product.objects.get(id=pid)
    my_cart, new_cart = Cart.objects.get_or_create(client=user, is_ordered=False)
    data = None
    if my_cart:
        count = CartItem.objects.filter(cart=my_cart, product=product).count()
        if count < 1:
            CartItem.objects.create(product=product, cart=my_cart)
            data = {
                'success': True,
                'product': product.name,
                'message': 'successfully added your cart!!!'
            }
        else:
            data = {
                'success': True,
                'product': product.name,
                'message': 'already your cart!!!'
            }
    elif new_cart:
        CartItem.objects.create(product=product, cart=new_cart)
        data = {
            'success': True,
            'product': product.name,
            'message': 'successfully added your cart!!!'
        }
    return JsonResponse(data, status=201)


def plus_quantity(request):
    cid = request.GET.get('_cid')
    cart_item = CartItem.objects.get(id=cid)
    cart_item.quantity += 1
    cart_item.save()
    data = {
        'success': True,
        'message': ' cart item incremented by 1',
    }
    return JsonResponse(data, status=200)


def minus_quantity(request):
    cid = request.GET.get('_cid')
    cart_item = CartItem.objects.get(id=cid)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        data = {
            'success': True,
        }
    else:
        cart_item.delete()
        data = {
            'success': True,
        }
    return JsonResponse(data, status=200)


def delete_cart_item(request):
    pk = request.GET.get('_cid')
    CartItem.objects.get(id=pk).delete()
    data = {
        'success': True
    }
    return JsonResponse(data, status=200)


@login_required
def checkout(request):
    cart_id = request.GET.get('cart_id')
    car = Cart.objects.filter(id=cart_id).first()
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = form.save(commit=False)
        order.cart = car
        order.client = request.user
        order.save()
        car.is_ordered = True
        car.save()
        messages.success(request, 'Successfully complated !!!')
        return redirect('.')
    ctx = {
        'form': form,
        'cart': car
    }
    return render(request, 'shop/checkout.html', ctx)

