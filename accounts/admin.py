from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.site_header = "Ecommerce Web App"
admin.site.site_title = "Ecom Admin"
admin.site.index_title = "Welcome to Our Site"
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_token','is_email_verified']
    model = Profile
# admin.site.register(Profile)