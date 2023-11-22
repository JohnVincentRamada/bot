from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from evsu_assistbot import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from authentication.forms import CaptchaForm, SetPasswordForm, PasswordResetForm
from django.db.models.query_utils import Q

from django.core.mail import send_mail
from authentication.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('a-bot')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
            

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            
            return redirect('a-bot')
        else:
            messages.error(request,"Wrong password or username")
            return redirect('login')
    
    return render(request, 'authentication/login.html')
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = none
        user.save()
    if user is not None and account_activation_token().check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"your account is successfully activated")
    else:
        messages.error(request,"link is invalid")
    return redirect('login')

def activate_email(request, myuser, to_email):
    
    subject = "Evsu Assist Bot Activation Account"
    message = render_to_string("authentication/template_activate_account.html", {
        'user': myuser,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': account_activation_token().make_token(myuser),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    to_list = [to_email]
    from_email = settings.EMAIL_HOST_USER
    email = send_mail(subject, message, from_email, to_list)
    if email > 0:
        messages.success(request, f'Hi {myuser}, please go to your email {to_email} inbox and click on the received activation link to complete registration.')
    else:
        messages.error(request, f'There\'s a problem sending an email to {to_email}, please check if you typed it correctly')
    

def register(request):

    # oxpa wfil mfxf yjny
    if request.user.is_authenticated:
        return redirect('a-bot')
    if request.method == "POST":
        
        username=request.POST["username"]
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        c_password = request.POST['c_password']

        if User.objects.filter(username=username):
            messages.error(request,"USERNAME ALREADY EXIST")
            return redirect('register')
        
        if User.objects.filter(email=email):
            messages.error(request,'EMAIL ALREADY EXISTS')
            return redirect('register')
        
        if password != c_password:
            messages.error(request,'PASSWORDS DO NOT MATCH!')
            return redirect('register')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.is_active=False
        myuser.save()
        mail = myuser.email
        activate_email(request, myuser, mail)
        

        # WELCOME MESSAGE
        subject = "Welcome to EVSU Assist Bot Chatbot for EVSU Carigara Campus!"
        message = "Hello " + myuser.first_name + "!! \n" + \
          "We're thrilled to have you join our online community. Our Chatbot is designed to make your \n" + \
          "experience at Eastern Visayas State University's Carigara Campus even more convenient \n" + \
          "and efficient. \n" + "\n" + \
          "Whether you're a student looking for course information, a faculty member in need of \n" + \
          "administrative support, or a visitor curious about campus events, EVSU Assist Bot is here to\n" + \
          "help.\n" + "\n" + \
          "With our user-friendly interface and the wealth of knowledge at your fingertips, you'll find\n" + \
          "answers to your questions faster. From campus resources to event \n" + \
          "schedules and general inquiries, we've got you covered.\n" + "\n" + \
          "Feel free to ask any questions or seek assistance at any time. Our mission is to make your \n" + \
          "journey at EVSU Carigara Campus as smooth and comfortable as possible.\n" + "\n" + \
          "Welcome aboard, and let's make your time at EVSU Carigara Campus truly exceptional!"

        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        

        return redirect('login')

    
    return render(request, 'authentication/registration.html')


def password_change(request):
    user = request.user
    form = SetPasswordForm(user)
    return render(request, 'authentication/password_reset_confrm.html',{'form':form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset"
                message = render_to_string("authentication/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token().make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                to_list = [associated_user.email]
                from_email = settings.EMAIL_HOST_USER
                email = send_mail(subject, message, from_email, to_list)
                if email > 0:
                    messages.success(request, f'Hi {associated_user.first_name}, please go to your email {associated_user.email} inbox and click on the received Reset link to complete resetting password.')
                else:
                    messages.error(request, f'Problem sendign reset password email')

            return redirect('login')

    form = PasswordResetForm()
    return render(
        request=request,
        template_name='authentication/password_reset.html',
        context={'form': form}
    )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token().check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and log in now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'authentication/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to login')
    
    return redirect('login')


def signout(request):
    logout(request)
    return redirect('login')