import random
import os
import json
import requests
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from django.utils import timezone

from friendship.models import Friend, FriendshipRequest
from simple_email_confirmation.models import EmailAddress
from six.moves import urllib
import shopify

from .choices import *
from .email import *
from .forms import *
from .models import *
from .redeem_points import *

def index(request):
    if not request.user.is_anonymous:return HttpResponseRedirect(reverse('challenge_list'))
    return render(request,'index.html')

def register(request,friend_id,organization_id):
    # if valid registration form, create user and send email confirmation.
    # user can't log in till email confirmed
    registered = False
    email = False
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            user = create_user(request,email)
            send_confirmation_email(request,user) # from email.py
            extra_user_fields(user,friend_id)
            registered = True
    else:
        form = UserForm(organization_id=organization_id)
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
        error = check_login(request)
        if not error: return HttpResponseRedirect(reverse('challenge_list'))

    # used for resend_email succesfully sent pop up
    try:
        sent = request.session['sent']
    except KeyError:
        sent = False
    return render(request,'login.html',{'error':error,'sent':sent})
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

@login_required
def challenge_list(request):
    user = request.user
    try:
        main_challenge = Challenge.objects.get(is_main_challenge=True)
    except ObjectDoesNotExist:
        main_challenge = False
    try:
        bonus_challenge = Challenge.objects.get(is_bonus_challenge=True)
    except ObjectDoesNotExist:
        bonus_challenge = False
    return render(request,'challenge_list.html',{
        'main':main_challenge,
        'bonus':bonus_challenge,
    })

@login_required
def challenge_detail(request,challenge_id):
    user = request.user
    challenge = Challenge.objects.get(pk=challenge_id)
    feelings = [random.choice(GROUP1_CHOICES),random.choice(GROUP2_CHOICES),random.choice(GROUP3_CHOICES)]
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            feeling = request.POST.get('feelingChoice')
            complete_challenge(user,challenge,form,feeling)
            return HttpResponseRedirect(reverse('challenge_list'))
    else:
        form = LocationForm()
    return render(request,'challenge_detail.html',{
        'challenge':challenge,
        'form':form,
        'feelings':feelings,
    })

@login_required
def accept_challenge(request,challenge_id):
    user = request.user
    challenge = Challenge.objects.get(pk=challenge_id)
    if not Challenge_Status.objects.filter(user=user,challenge=challenge).exists():
        Challenge_Status.objects.create(user=user,challenge=challenge,status=2)
    return HttpResponseRedirect(reverse('challenge_list'))

@login_required
def act_entry(request):
    user = request.user
    if request.method == 'POST':
        form = ActForm(request.POST)
        if form.is_valid():
            complete_act(user,form)
            return HttpResponseRedirect(reverse('challenge_list'))
    else:
        form = ActForm()
    return render(request,'act_entry.html',{
        'form':form,
    })

@login_required
def my_activity(request):
    user = request.user
    activities = user.get_activities()
    return render(request,'my_activity.html',{
        'user':user,
        'activities':activities,
    })

@login_required
def friend_request(request):
    user = request.user
    sent = False
    already_friends = False
    if request.method == 'POST':
        email = request.POST.get('email')
        msg = 'Hi! ' + user.get_full_name() + ' would like to add you!'
        try:
            other_user = User.objects.get(email=email)
            if not Friend.objects.are_friends(user, other_user) == True:
                Friend.objects.add_friend(
                    request.user,  # sender
                    other_user,    # recipient
                    message=msg
                )
                sent = True
            else:
                already_friends = True
        except ObjectDoesNotExist:
            send_request_email(request,user,email)
            sent = True
    return render(request,'friend_request.html',{
        'sent':sent,
        'already':already_friends,
    })

@login_required
def friend_activity(request):
    user = request.user
    friends = Friend.objects.friends(user)
    requests = Friend.objects.unrejected_requests(user=user)
    return render(request,'friend_activity.html',{
        'friends':friends,
        'requests':requests,
    })

@login_required
def accept_reject_request(request,request_id,accept):
    friend_request = FriendshipRequest.objects.get(pk=request_id)
    friend_request.accept() if int(accept) == 1 else friend_request.reject()
    return HttpResponseRedirect(reverse('friend_activity'))

@login_required
def remove_friend(request,friend_id):
    user = request.user
    friend = User.objects.get(pk=friend_id)
    Friend.objects.remove_friend(user, friend)
    return HttpResponseRedirect(reverse('friend_activity'))

@login_required
def redeem_points(request):
    user = request.user
    error = False
    if request.method == 'POST':
        points = request.POST.get('points')
        error = check_points(points,user)
        if not error:
            cash = '%.2f' % (int(points)/100)
            discount_code = create_discount(cash)
            if discount_code:
                return HttpResponseRedirect(reverse('redeem_confirmation',kwargs={'discount_code':discount_code,'value':cash,'points':points}))
            else:
                error = 'Something strange has happened, contact an administrator!'
    return render(request, 'redeem_points.html',{
        'user':user,
        'error':error
    })

@login_required
def redeem_confirmation(request,discount_code,value,points):
    user = request.user
    User.objects.filter(pk=request.user.id).update(redeemed_points=F('redeemed_points')+points)
    send_redeem_points_email(user,discount_code,value,points)
    return render(request, 'redeem_confirmation.html',{
        'value':value,
        'points':points,
    })
########## HELPERS ###########

def check_login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if EmailAddress.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.check_password(password):
            if user.is_confirmed:
                auth_login(request, user)
            else:
                return confirmation_error(request,user)
        else:
            return incorrect_pass() # from email.py
    else:
        return email_does_not_exist() # from email.py
    return False
def create_user(request,email):
    user = User.objects.create_user(
        email,
        email=email,
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        zip_code=request.POST.get('zip_code'),
        organization=Organization.objects.get(pk=request.POST.get('organization')),
        password=request.POST.get('password'),
    )
    return user

def extra_user_fields(user,friend_id):
    if User.objects.filter(pk=friend_id).exists():
        # if registering from friend request email
        friend = User.objects.get(pk=friend_id)
        Friend.objects.add_friend(friend,user)

def complete_challenge(user,challenge,form,feeling):
    location_form = form.save(commit=False)
    location = Location.objects.get_or_create(
        address=location_form.address, city=location_form.city,
        state=location_form.state, zip_code=location_form.zip_code
    )[0]
    challenge_status = Challenge_Status.objects.filter(user=user,challenge=challenge)
    challenge_status.update(status=3)
    challenge_status.update(location=location)
    challenge_status.update(feeling=feeling)
    challenge_status.update(date_completed=timezone.now())

def complete_act(user,form):
    public = form.cleaned_data['public']
    act = form.save(commit=False)
    act.user = user
    act.public = public
    act.save()

def check_points(points,user):
    if points is '':
        return 'Please fill in the number of points to redeem'
    if int(points) < 0 or int(points) > user.get_points():
        return 'Please fill in a valid number of points'
    if int(points) % 5 != 0:
        return 'Please make your points divisible by 5'
    return False
