from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from simple_email_confirmation.models import EmailAddress

from .models import *
from .forms import *
from .email import *

def index(request):
    return render(request,'index.html')

def register(request):
    # if valid registration form, create user and send email confirmation.
    # user can't log in till email confirmed
    registered = False
    email = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = User.objects.create_user(
                email,
                email=email,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                zip_code=request.POST.get('zip_code'),
                password=request.POST.get('password'),
                points=0,
            )
            send_confirmation_email(request,user) # from email.py
            registered = True

    else:
        form = UserForm()
    return render(request, 'register.html',{
        'form':form,
        'registered':registered,
        'email':email,
    })
def confirm_email(request,user_id,confirmation_key):
    # check if confirmation key matches users email key,
    # confirm email if it does.
    error = False
    try:
        user = User.objects.get(id=user_id)
        email = EmailAddress.objects.get(email=user.email)
        if confirmation_key == email.key:
            user.confirm_email(confirmation_key)
            auth_login(request, user)
        else:
            error = confirmation_error(request,user) # from email.py
    except ObjectDoesNotExist:
        error = confirmation_error(request,user) # from email.py
    return render(request, 'confirm_email.html',{'error':error})
def resend_email(request,email):
    # reset users confirmation key and resend email
    email_address = EmailAddress.objects.get(email=email)
    email_address.reset_confirmation()
    user = User.objects.get(email=email)
    send_confirmation_email(request,user) # from email.py
    request.session['sent'] = True # to have email sent pop up on login page
    return HttpResponseRedirect(reverse('login'))
def login(request):
    error = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if EmailAddress.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_confirmed:
                    error = False
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    error = confirmation_error(request,user) # from email.py
            else:
                error = incorrect_pass() # from email.py
        else:
            error = email_does_not_exist() # from email.py
    # used for resend_email succesfully sent pop up
    try:
        sent = request.session['sent']
    except KeyError:
        sent = False
    return render(request,'login.html',{'error':error,'sent':sent})
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
