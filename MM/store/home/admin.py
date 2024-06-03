from django.contrib import admin
from .models import Profile, Contact, Billing_address, Shipping_address, Coupon, Item, Order

# Register your models here.
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Shipping_address)
admin.site.register(Billing_address)
admin.site.register(Coupon)
admin.site.register(Item)
admin.site.register(Order)
