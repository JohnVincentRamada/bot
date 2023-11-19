from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from evsu_assistbot import settings
from django.core.mail import send_mail
# Create your views here.

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('a-bot')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # return render(request, 'a-bot.html')
            return redirect('a-bot')
        else:
            messages.error(request,"Wrong password or username")
            return redirect('login')

    return render(request, 'authentication/login.html')
    


    

def register(request):

    # oxpa wfil mfxf yjny
    if request.user.is_authenticated:
        return redirect('a-bot')
    if request.method == "POST":
        # email = request.POST.get['email']
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

        myuser.save()
        messages.success(request, "Your account has been registered")

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
def signout(request):
    logout(request)
    return redirect('login')