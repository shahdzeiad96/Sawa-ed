from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import *

# Create your views here.
def index(request):
    return render(request,"guesthome.html")


def register(request):
    if request.method == 'POST':
        username         = request.POST.get('username')
        email            = request.POST.get('email')
        password         = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration/register.html")
        
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "A user with that username or email already exists.")
            return render(request, "register.html")
    else:
        return render(request, "registration/register.html")

def login(request):
    if request.method == 'POST':

        email    = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('/')  # we should redirect to home page
        else:
            messages.error(request, "Invalid login credentials.")
            return render(request, "login.html")
    else:
        return render(request, "login.html")