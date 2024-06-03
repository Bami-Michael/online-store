from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from home.models import Contact, Item, Profile, Order, Shipping_address, Billing_address
from cart.cart import Cart
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
import stripe
import json
import time




def my_shipping(request):
    shipping_address = get_object_or_404(Shipping_address, user= request.user)
    return f'{shipping_address.first_name} {shipping_address.last_name}\n{shipping_address.address}\n{shipping_address.city}\n{shipping_address.state}\n{shipping_address.zip}\n{shipping_address.country}\n{shipping_address.phone}'



def my_billing(request):
    billing_address = get_object_or_404(Billing_address, user= request.user)
    return f'{billing_address.first_name} {billing_address.last_name}\n{billing_address.address}\n{billing_address.city}\n{billing_address.state}\n{billing_address.zip}\n{billing_address.country}\n{billing_address.phone}'




@login_required(login_url="sign_in")
def success(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    #customer = stripe.Customer.retrieve(session.customer)
    ship = Shipping_address.objects.get(user = request.user)
    bill = Billing_address.objects.get(user = request.user)
    item_cart = Cart(request)
    profile = Profile.objects.get(user__id=request.user.id)
    cart = profile.old_cart
    current_order = Order.objects.filter(stripe_id=checkout_session_id)
    if current_order:
        pass
    else:
        order = Order.objects.create(user = request.user, 
                                    OrderItems = cart,
                                    total = item_cart.total(),
                                    stripe_id = checkout_session_id,
                                    shipping_info = my_shipping(request),
                                    billing_info = my_billing(request)
                                    )
        profile.old_cart = None
        profile.save()
        request.session['session_key'] = {}
    return render(request, 'success.html', {} )


def failed(request):
    return render(request, 'failed.html', {} )


@login_required(login_url="sign_in")
def payment(request):
    shipping = Shipping_address.objects.filter(user=request.user).first()
    billing = Billing_address.objects.filter(user=request.user).first()
    if shipping is None and billing is None:
        messages.success(request, 'Please set the shipping and billing address to proceed to checkout.')
        return redirect('cart')
    else:
        cart = Cart(request)
        session = request.session
        cart_id = cart.cart.keys()
        cart_dict = request.session['session_key']
        products = Item.objects.filter(id__in = cart_id) 
        filtered_session = {int(key): get_object_or_404(Item, id=key).price()*value for key, value in cart.cart.items()}
        total = 0
        for value in filtered_session.values():
            total += Decimal(value)
        print(shipping)
        return render(request, 'checkout.html', {'products':products, 'session':session, "subtotal":filtered_session, 'total':total, 'cart_dict':cart_dict, 'shipping':shipping, 'billing':billing} )



@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    


@csrf_exempt
def create_checkout_session(request):    
    cart = Cart(request) 
    total = cart.total()
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(total)*100,
                        "product_data": {
                            "name": 'Cosmetic Products',
                            "description": 'BeBold Cosmetic Stored Order',
                            
                        },
                    },
                    "quantity": 1,
                }
            ],
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        



@csrf_exempt
def stripe_webhook(request):
    time.sleep(20)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    payload = request.body

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        session = event['data']['object']
        session_id = session.get('id',None)
        #time.sleep(10)
        # Extract the Stripe ID from the session
        order = get_object_or_404(Order, stripe_id= session_id)
        order.payment_received = True
        order.save()

    return HttpResponse(status=200)