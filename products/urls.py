from django.urls import path
from . import views

urlpatterns = [
    path('<slug>/',views.get_products,name="products_info"),
    path('',views.products,name="products"),
    path('add-to-cart/<uid>',views.add_to_cart,name="add_to_cart"),
    path('remove-from-cart/<cart_item_uid>',views.remove_cartitem,name="remove_cartitem"),
    # path('remove-cart',views.remove_cart, name="remove_cart")
]