import random
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from friendship.models import Friend, FriendshipRequest
from simple_email_confirmation.models import EmailAddress

from .choices import *
from .email import *
from .forms import *
from .models import *

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
            create_user(request,email)
            send_confirmation_email(request,user) # from email.py
            # ~~~ For Testing ~~~~
            # email = EmailAddress.objects.get(email=user.email)
            # user.confirm_email(email.key)
            # auth_login(request, user)
            # ~~~~~~~~~~~~~~~~~~~
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
    main_challenge = Challenge.objects.get(is_main_challenge=True)
    bonus_challenge = Challenge.objects.get(is_bonus_challenge=True)
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
    if request.method == 'POST':
        email = request.POST.get('email')
        msg = 'Hi! ' + user.get_full_name() + ' would like to add you!'
        try:
            other_user = User.objects.get(email=email)
            Friend.objects.add_friend(
                request.user,  # sender
                other_user,    # recipient
                message=msg
            )
        except ObjectDoesNotExist:
            pass
    return render(request,'friend_request.html',{
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
