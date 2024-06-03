from home.models import Item, Profile
from django.shortcuts import get_object_or_404
import json
from decimal import Decimal


class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

        plist = self.session.get('price_list')
        if 'price_list' not in request.session:
            self.session['price_list'] = 0.00
            plist = self.session['price_list']

        self.plist = plist


        carty = self.session.get('carty')
        if 'carty' not in request.session:
            carty = self.session['carty'] = []

        self.carty = carty


    def __len__(self):
        return len(self.cart)
    



    def adder(self, product):
        cart_list = self.carty
        qty = self.session.get(str(product.id))
        #qty = self.session[product.id]
        items = product.id
        if items in cart_list:
            pass
        else:
            cart_list.append(items)
            self.session['carty'] = cart_list  
        if qty and qty <= 4:
            qty += 1
        elif qty == 5:
            qty = 5
        else:
            qty = 1
        if str(items) in self.cart:
            if self.cart[str(items)] < 5:
                self.cart[str(items)]+=1      
        else:
            self.cart[str(items)] = 1
        self.session[int(product.id)] = qty  
        self.session['session_key'] = self.cart  
        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            kart = str(self.cart)
            replaced_cart = kart.replace("\'", "\"")
            current_user.update(old_cart = replaced_cart)
    


    def deleter(self, product):
        cart_list = self.carty
        cart_dict = self.cart
        qty = self.session.get(str(product.id))
        item = product.id
        if item in cart_list:
            cart_list.remove(item)
            self.session['price_list'] -= (int(product.price())*int(qty))
            self.session['carty'] = cart_list  
        if qty:
            self.session.pop(str(product.id))
        if str(item) in cart_dict:
            cart_dict.pop(str(item))
            self.session['session_key'] = cart_dict 
        self.session.modified = True



    def total(self):
        filtered_session = {int(key): get_object_or_404(Item, id=key).price()*value for key, value in self.cart.items()}
        total = 0
        for value in filtered_session.values():
            total += Decimal(value)
        return total



    
    