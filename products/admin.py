from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)
# admin.site.register(Order)

@admin.register(Sizevariant)
class SizevariantAdmin(admin.ModelAdmin):
    list_display = ['size','price']
    model = Sizevariant
@admin.register(Colorvariant)
class Colorvariant(admin.ModelAdmin):
    list_display = ['color','price']
    model = Colorvariant

admin.site.site_header = "Ecommerce Web App"
admin.site.site_title = "Ecom Admin"
admin.site.index_title = "Welcome to Our Site"

