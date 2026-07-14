from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('place-order/', views.place_order, name='place_order'),
]
