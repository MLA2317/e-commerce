from django.shortcuts import render
from .models import Product
from apps.blogs.models import Post
from django.contrib.auth.decorators import login_required


def index(request):
    posts = Post.objects.order_by('-id')[:3]
    product = Product.objects.all().order_by('-id')
    top_rated_products = product.order_by('-mid_rate')[:6]
    top_viewed_products = product.order_by('-views')[:6]
    latest_products = product[:6]
    s = request.GET.get('s')
    if s:
        product = Product.objects.filter(name__icontains=s)
    ctx = {
        'products': product[:8],
        'posts': posts,
        'latest_products': latest_products,
        'top_rated_products': top_rated_products,
        'top_viewed_products': top_viewed_products,
    }
    return render(request, 'product/index.html', ctx)


@login_required
def shop_details(request, pid):
    product = Product.objects.get(id=pid)
    related_products = Product.objects.order_by('-id')[:4]
    ctx = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/shop-details.html', ctx)


@login_required
def shop_grid(request):
    products = Product.objects.order_by('-id')[:12]
    last_products = Product.objects.order_by('-id')[:6]
    s = request.GET.get('s')
    if s:
        products = Product.objects.filter(name__icontains=s)
    cat = request.GET.get('cat')
    if cat:
        products = Product.objects.filter(category__category__exact=cat)
    ctx = {
        'products': products,
        'last_products': last_products
    }
    return render(request, 'shop/shop-grid.html', ctx)


