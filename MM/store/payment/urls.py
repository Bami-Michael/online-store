from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment, name='payment'),
    path('success', views.success, name='success'),
    path('failed', views.failed, name='failed'),
    path('webhook/', views.stripe_webhook),
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
]
