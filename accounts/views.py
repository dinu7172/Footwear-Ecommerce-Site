
from cmath import log
from tkinter import E
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import imp
from .models import Profile
from base.emails import *
import re


def user_login(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')

def logout_user(request):
    # user = request.user
    logout(request)
    return redirect('/')


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"

# compiling regex
match_re = re.compile(reg)

# searching regex


# validating conditions

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if(re.fullmatch(regex, email)):
            if re.search(match_re, password):
                user_obj = User.objects.filter(username = email)
                if user_obj.exists():
                    messages.warning(request, "The email is already exist.")
                    return HttpResponseRedirect(request.path_info)

                user_obj = User.objects.create(first_name=first_name,last_name=last_name,email=email, username=email)
                user_obj.set_password(password)
                user_obj.save()
                print(user_obj.email)
                messages.success(request, "The email has been sent you to mail.")
            else:
                messages.warning(request, "The password is not valid")
        else:
            messages.warning(request, "The name is not valid")   
    


        return HttpResponseRedirect(request.path_info)

    return render(request,'accounts/signup.html')

def activate_user(request,email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')

    except Exception as e:
        return HttpResponse("Invalid Token")

def forget_password(request):
    if request.method =="POST":
        email = request.POST.get('email')
        user_obj = User.objects.filter(username = email)
        print(user_obj.exists())
        if user_obj.exists():
            
            # user = User.objects.filter(email=email)
            et = Profile.objects.get(user__email=email)
            email_token = et.email_token

            # print(email_token)
            
            # message = f'Hi, click on the link to change your account password http://127.0.0.1:8000/accounts/change/{email_token}'
            send_forget_email(email,email_token)
            # return send_mail(subject , message , email_from , [email])
            messages.success(request, "The email has been sent you to mail.")
            return HttpResponseRedirect(request.path_info)
        else:
            messages.warning(request, "The email dont't exists")
            return HttpResponseRedirect(request.path_info)


    return render(request,"accounts/forget_pswd.html")

def change_pswd(request, email_token):
    if request.method == "POST":
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        print(pass1,pass2)
        if pass1 !=pass2:
            messages.warning(request, "Passwords is not matching")
            return HttpResponseRedirect(request.path_info)
        if re.search(match_re, pass1):
            user = Profile.objects.get(email_token=email_token)
            user = user.user
            email = user.email
            user = User.objects.get(username=email)
            user.set_password(pass2)
            user.save()
        else:
            messages.warning(request, "Password is not valid.")
            return HttpResponseRedirect(request.path_info)
        
        return redirect('login')
    return render(request, "accounts/change.html")