from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('log_out', views.log_out, name='log_out'),
    path('store', views.store, name='store'),
    path('profile', views.profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('contact', views.contact, name='contact'),
    path('item/<int:pk>', views.item, name='item'),
    path('edit_password', views.edit_password, name='edit_password'),
    path('edit_shipping', views.edit_shipping, name='edit_shipping'),
    path('edit_billing', views.edit_billing, name='edit_billing'),
]