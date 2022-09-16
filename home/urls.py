from django.urls import path
from . import views
from products.views import cart,add_to_cart, remove_coupon, success

urlpatterns = [
    path('',views.index,name='index'),
    path('cart/',cart,name="cart"),
    # path('add-to-cart/<uid>',add_to_cart,name="add_to_cart"),
    path('remove_coupon/<cart_id>/',remove_coupon ,name="remove_coupon"),
    path('success/',success,name="payment_success"),
 

]