from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.html import format_html

from .models import *

def incorrect_pass():
    return "Your username and password didn't match."

def email_does_not_exist():
    return "No accounts with that email exist."

def confirmation_error(request,user,):
    # create confirmation error message with button to resend email
    href = reverse('resend_email', args=[user.email])
    msg = "Make sure you are using the most recent confirmation email."
    error = format_html(msg+'<br><a href="' + href +  '">Click to resend</a> confirmation email')
    return error
def send_confirmation_email(request,user):
    # build confirmation email with confirmation_email_template and send it
    url = request.build_absolute_uri(reverse('confirm_email', args=[user.id,user.confirmation_key]))
    context = {'user': user,'url':url}
    text_content = 'plaintext'
    html = get_template('confirmation_email_template.html')
    html_content = html.render(context)
    email = EmailMultiAlternatives("Welcome to Be A!", text_content, to=[user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()
