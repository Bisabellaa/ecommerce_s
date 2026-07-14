from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Variation
from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = _cart_id(request)
    cart, _ = Cart.objects.get_or_create(cart_id=cart_id)

    selected_variations = Variation.objects.filter(
        id__in=[request.POST.get('color'), request.POST.get('size')]
    )

    cart_items = CartItem.objects.filter(
        product=product,
        cart=cart,
        is_active=True,
    )

    matching_item = None
    for ci in cart_items:
        ci_var_ids = list(ci.variations.all().values_list('id', flat=True).order_by('id'))
        sel_var_ids = list(selected_variations.values_list('id', flat=True).order_by('id'))
        if ci_var_ids == sel_var_ids:
            matching_item = ci
            break

    if matching_item:
        matching_item.quantity += 1
        matching_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
        )
        cart_item.variations.set(selected_variations)

    return redirect('cart')


def remove_cart_item(request, cart_item_id):
    cart_id = _cart_id(request)
    cart = Cart.objects.filter(cart_id=cart_id).first()
    if cart:
        cart_item = CartItem.objects.filter(
            id=cart_item_id,
            cart=cart,
            is_active=True,
        ).first()
        if cart_item:
            cart_item.delete()
    return redirect('cart')


def update_cart(request, cart_item_id):
    cart_id = _cart_id(request)
    cart = Cart.objects.filter(cart_id=cart_id).first()
    if cart and request.method == 'POST':
        action = request.POST.get('action')
        cart_item = CartItem.objects.filter(
            id=cart_item_id,
            cart=cart,
            is_active=True,
        ).first()
        if cart_item:
            if action == 'plus':
                cart_item.quantity += 1
            elif action == 'minus':
                cart_item.quantity -= 1
                if cart_item.quantity < 1:
                    cart_item.quantity = 1
            else:
                quantity = request.POST.get('quantity')
                if quantity is not None:
                    try:
                        quantity = int(quantity)
                        if quantity < 1:
                            quantity = 1
                    except ValueError:
                        quantity = 1
                    cart_item.quantity = quantity
            cart_item.save()
    return redirect('cart')


def _get_cart_data(request):
    cart_id = _cart_id(request)
    cart = Cart.objects.filter(cart_id=cart_id).first()

    cart_items = []
    total = Decimal('0')
    iva = Decimal('0')
    grand_total = Decimal('0')

    if cart:
        cart_items = CartItem.objects.filter(
            cart=cart,
            is_active=True,
        ).order_by('product__product_name')

        for item in cart_items:
            total += item.sub_total()

    iva = round(total * Decimal('0.10'), 2)
    grand_total = round(total + iva, 2)

    return {
        'cart_items': cart_items,
        'total': total,
        'iva': iva,
        'grand_total': grand_total,
    }


def cart(request):
    context = _get_cart_data(request)
    return render(request, 'cart/cart.html', context)


def place_order(request):
    context = _get_cart_data(request)
    return render(request, 'cart/place-order.html', context)
