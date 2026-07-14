from django.db.models import Sum
from .models import Cart, CartItem


def cart_count(request):
    count = 0
    if 'admin' in request.path:
        return {'cart_count': count}
    try:
        cart_id = request.session.session_key
        if cart_id:
            cart = Cart.objects.filter(cart_id=cart_id).first()
            if cart:
                result = CartItem.objects.filter(
                    cart=cart, is_active=True
                ).aggregate(Sum('quantity'))
                count = result['quantity__sum'] or 0
    except:
        count = 0
    return {'cart_count': count}
