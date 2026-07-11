from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def store(request):
    return render(request, 'store.html')

def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request, 'register.html')

def cart(request):
    return render(request, 'cart.html')

def product_detail(request):
    return render(request, 'product-detail.html')

def place_order(request):
    return render(request, 'place-order.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def search_result(request):
    return render(request, 'search-result.html')

def order_complete(request):
    return render(request, 'order_complete.html')