from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add', views.add, name='add'),# type: ignore
    path('cart_delete', views.cart_delete, name='cart_delete'),# type: ignore
    path('cart_update', views.cart_update, name='cart_update'),
    
]