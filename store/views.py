from django.db import models
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Product
from category.models import Category
from cart.models import Cart, CartItem


def store(request, category_slug=None):
    keyword = request.GET.get('keyword', '')

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    if keyword:
        products = products.filter(
            models.Q(product_name__icontains=keyword) |
            models.Q(description__icontains=keyword)
        )

    product_count = products.count()

    paginator = Paginator(products, 6)
    page = request.GET.get('page')

    try:
        paged_products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        paged_products = paginator.page(1)

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug=None):
    if slug:
        product = get_object_or_404(Product, slug=slug)
    else:
        product = Product.objects.filter(is_available=True).first()

    in_cart = False
    cart_id = request.session.session_key
    if cart_id:
        cart = Cart.objects.filter(cart_id=cart_id).first()
        if cart:
            in_cart = CartItem.objects.filter(
                cart=cart, product=product, is_active=True
            ).exists()

    variations = product.variation_set.filter(is_active=True)
    colors = variations.filter(variation_category='color')
    sizes = variations.filter(variation_category='talle')

    context = {
        'product': product,
        'in_cart': in_cart,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, 'store/product-detail.html', context)
