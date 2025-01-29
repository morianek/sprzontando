from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Email lub hasło są nieprawidłowe')
    return render(request, 'authentication/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        print(request.POST)
        return redirect('main')
    return render(request, 'authentication/register.html')

def log_out(request):
    logout(request)
    return redirect('main')

def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'settings/user_settings.html')

def site_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'settings/site_settings.html')