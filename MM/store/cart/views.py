from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from .cart import Cart
from home.models import Item, Profile
from django.http import JsonResponse
from decimal import Decimal






def cart(request):
    cart = Cart(request)
    session = request.session
    cart_id = cart.cart.keys()
    products = Item.objects.filter(id__in = cart_id)
    total = cart.total()
    len = cart.__len__()
    item_qty = session['session_key']
    #dict comprehension to filter the session for keys with lenght of 1,
    #it changes the keys to integers and the values to price * quantity of item
    filtered_session = {int(key): get_object_or_404(Item, id=key).price()*value for key, value in cart.cart.items()}
    return render(request, 'cart.html', {'products':products, 'session':session, "subtotal":filtered_session, 'total':total, 'len':len, 'item_qty':item_qty} )

 

    


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Item, id=product_id)
        cart.adder(product=product)
        cart_qty = cart.__len__()
        total = cart.total()
        response = JsonResponse({'ProductName':product.title, 'qty':cart_qty,'price':total})       
        return response
    
 

def cart_delete(request):
    cart = Cart(request)
    cart_id = cart.carty
    if request.method == 'POST':
        id_of_item = request.POST["item_id"]
        product = get_object_or_404(Item, id=id_of_item)
        cart.deleter(product)
        product = Item.objects.filter(id__in = cart_id)
        #deal with logged in user
        if request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=request.user.id)
            kart = str(cart.cart)
            replaced_cart = kart.replace("\'", "\"")
            current_user.update(old_cart = replaced_cart)
    return redirect('cart')



def cart_update(request):
    cart = Cart(request)
    session = request.session
    item_dict = request.session.get('session_key')
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        product_price = get_object_or_404(Item, id=product_id).price()
        session[product_id] = int(product_qty)
        subtotal = product_price*int(product_qty)
        item_dict[str(product_id)] = int(product_qty)
        request.session['sessionkey'] = item_dict
        total = cart.total()
        #deal with logged in user
        if request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=request.user.id)
            kart = str(cart.cart)
            replaced_cart = kart.replace("\'", "\"")
            current_user.update(old_cart = replaced_cart)
        response = JsonResponse({"subtotal":subtotal, 'total':total })       
        return response
    







