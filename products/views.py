from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from products.models import *
from django.contrib import messages
import razorpay

# Create your views here.
def products(request):
    products = Product.objects.all()
    return render(request,'products/products.html',{
        'products':products
    })
    
def get_products(request,slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {'product':product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            # print(size)
            price = product.get_product_by_size(size)
            # print(price)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request,"products/pro_info.html",context=context)

    except Exception as e:
        print(e)

def add_to_cart(request, uid):
    variant = request.GET.get('variant')
    cart , _ = Cart.objects.get_or_create(user= request.user, is_paid=False)
    product = Product.objects.get(uid = uid)
    
    
    cart_items = CartItem.objects.filter(product=product)
    # if cart_items.exists():
    #     CartItem.objects.filter(product=product)[0].quantity = CartItem.objects.filter(product=product)[0].quantity + 1
    #     CartItem.objects.filter(product=product)[0].save()
    # else:
        
    cart_items = CartItem.objects.create(cart=cart,product=product)
    if variant:
        variant = request.GET.get('variant')
        size_variant = Sizevariant.objects.get(size = variant)
        cart_items.Sizevariant = size_variant
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cartitem(request, cart_item_uid):
    try:
        cart_item = CartItem.objects.get(uid=cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# def update_qnt(request, cart_items):
#     cart_item.quantity = 

from django.conf import settings
def cart(request):
    cart = None
    try:
        cart = Cart.objects.get(user=request.user,is_paid=False)
    except Exception as e:
        print(e)
    context = {'cart_items': CartItem.objects.filter(cart__is_paid=False,cart__user=request.user)}
    # cart = Cart.objects.get(user=request.user,is_paid=False)
    context['cart'] = cart
    if request.method  == 'POST':
        
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon)
        if not coupon_obj.exists():
            messages.warning(request,'Invalid Coupon Code')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.coupon:
            messages.warning(request,'Coupon code is already applied.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart.get_cart_total() < Coupon.objects.get(coupon_code__icontains=coupon).minimum_amount:
            messages.warning(request,f"The Amount should be greater then {Coupon.objects.get(coupon_code__icontains=coupon).minimum_amount}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_obj[0].is_expired:
            messages.warning(request,'expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart.coupon = coupon_obj[0]
        cart.save()
        messages.success(request,'Coupon applied Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # context['cartitems']= CartItem.objects.filter(cart=cart)
    if cart:
        client = razorpay.Client(auth =(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount':cart.get_cart_total()*100,'currency':'INR','payment_capture':1})
        # order = Order.objects.get(cart = cart)
        cart.razorpay_order_id = payment['id']
        cart.save()
        print('**********************')
        print(payment)
        print('**********************')
        
    else:
        payment = None
    context['payment'] = payment
    print(payment)
    return render(request,"products/cart.html",context)



def remove_coupon(request, cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon  = None
    cart.save()
    messages.success(request,'Coupon removed Successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
    order_id = request.GET.get('razorpay_order_id')
    cart = Cart.objects.get(razorpay_order_id=order_id)
    # order = Order.objects.get(razorpay_order_id=order_id)
    cart.is_paid = True
    cart.save()
    return HttpResponse("Paymnet Successful")





