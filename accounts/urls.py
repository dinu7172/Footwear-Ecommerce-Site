from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('signup/',views.register, name="register"),
    path('activate/<email_token>/',views.activate_user,name="activate"),
    path('forget_password', views.forget_password,name="forget"),
    path('change/<email_token>/',views.change_pswd,name="change"),
    path('logout',views.logout_user,name='logout')

]