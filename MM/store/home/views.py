from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contact, Item, Profile, Shipping_address, Billing_address, Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from cart.cart import Cart
from decimal import Decimal
import json





def home(request):
    cart = Cart(request)
    cart_len = cart.__len__()
    total_price = cart.total()
    trending = Item.objects.all()[:4]
    best_selling = Item.objects.all()[4:8]
    return render(request, 'index.html', {'best_selling':best_selling, 'trending':trending, 'len':cart_len, 'total':total_price} )


@login_required(login_url="sign_in")
def profile(request):
    cart = Cart(request)
    cart_len = cart.__len__()
    total_price = cart.total()
    shipping = Shipping_address.objects.filter(user = request.user).first()
    billing = Billing_address.objects.filter(user = request.user).first()
    orders = Order.objects.filter(user = request.user)  
    return render(request, 'profile.html', {'shipping':shipping, 'billing':billing, 'orders':orders, 'len':cart_len, 'total':total_price} )




@login_required(login_url="sign_in")
def profile_edit(request):
    return render(request, 'profile_edit.html', {} )




@login_required(login_url="sign_in")
def edit_password(request):
    current_user = request.user.email
    user = User.objects.get(email=current_user)
    if request.method == 'POST':
        old_pass = request.POST['old_pass']  
        new_pass1 = request.POST['new_pass1'] 
        new_pass2 = request.POST['new_pass2']
        if new_pass1 == new_pass2:
            user.set_password(new_pass1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, ("Password changed successfully..."))
        else:
            messages.success(request, ("New password did not match,Please try again..."))
    return redirect("profile")



@login_required(login_url="sign_in")
def edit_shipping(request):
    shipping = Shipping_address.objects.filter(user = request.user).first()
    if request.method == 'POST':
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name'] 
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        country = request.POST['country']
        phone = request.POST['phone']
        if shipping:
            shipping.first_name = first_name
            shipping.last_name = last_name
            shipping.address = address
            shipping.city = city
            shipping.state = state
            shipping.zip = zip
            shipping.country = country
            shipping.phone = phone
            shipping.save()
            messages.success(request, ("Shipping Address updated successfully..."))
        else:
            shipping = Shipping_address(
                user = request.user,
                first_name = first_name,
                last_name = last_name,
                address = address,
                city = city,
                state = state,
                zip = zip,
                country = country,
                phone = phone
                )
            shipping.save()
            messages.success(request, ("Shipping Address created successfully..."))
    return redirect("profile")



@login_required(login_url="sign_in")
def edit_billing(request):
    billing = Billing_address.objects.filter(user = request.user).first()
    if request.method == "POST":
        first_name = request.POST['first_name']  
        last_name = request.POST['last_name'] 
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        country = request.POST['country']
        phone = request.POST['phone']
        if billing:
            billing.first_name = first_name
            billing.last_name = last_name
            billing.address = address
            billing.city = city
            billing.state = state
            billing.zip = zip
            billing.country = country
            billing.phone = phone
            billing.save()
            messages.success(request, ("Billing Address updated successfully..."))
        else:
            billing = Billing_address(
                user = request.user,
                first_name = first_name,
                last_name = last_name,
                address = address,
                city = city,
                state = state,
                zip = zip,
                country = country,
                phone = phone
                )
            billing.save()
            messages.success(request, ("Billing Address created successfully..."))
    return redirect("profile") 



    

def sign_up(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        username = request.POST["username"]      
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)                        
            login(request, user)
            request.session.set_expiry(3000)
            current_user = Profile.objects.filter(user=request.user)
            cart = Cart(request)
            kart = str(cart.cart)
            replaced_cart = kart.replace("\'", "\"")
            current_user.update(old_cart = replaced_cart)
            return redirect(store)
        else:
            messages.success(request, ("Your password did not match, please Try Again..."))
            return  redirect(sign_up)        
    else:
        return render(request, 'sign-up.html', {} )




 
def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            #request.session.set_expiry(3000)
            login(request, user)
            profile = Profile.objects.get(user__id=request.user.id)
            cart = profile.old_cart
            if cart:
                data = json.loads(cart)
                request.session['session_key'] = data   
                request.session['carty'] = list(request.session['session_key'])                
            return  redirect(store)
        else:
            messages.success(request, ("Invalid Login Credentials, Try Again..."))
            return  redirect(sign_in)
        
    return render(request, 'sign-in.html', { } )



def log_out(request):
    logout(request)    
    return redirect("home")


 
def store(request):
    cart = Cart(request)
    cart_len = cart.__len__()
    total_price = cart.total()
    items = Item.objects.all()
    return render(request, 'store.html', {"items":items, 'len':cart_len, 'total':total_price} )






def item(request, pk):
    item = Item.objects.get(id=pk)
    cart = Cart(request)
    cart_len = cart.__len__()
    caty = cart.carty
    total_price = cart.total()
    return render(request, 'item.html', {"item":item, 'cart_len':cart_len, "total_price":total_price , 'caty':caty} )



def contact(request):
    cart = Cart(request)
    cart_len = cart.__len__()
    total_price = cart.total()
    if request.method == 'POST':
        first = request.POST["first"]
        email = request.POST["email"]
        last = request.POST["last"]
        message = request.POST["message"]
        form = Contact(first=first, email=email, last=last, message=message)
        form.save() 
        messages.success(request, 'Message Sent! We will get back to you as soon as possible!')
        return redirect(contact)
    return render(request, 'contact.html', {'len':cart_len, 'total':total_price} )








