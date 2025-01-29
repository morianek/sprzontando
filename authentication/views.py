from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import CustomUser

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

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username == request.user.username and email == request.user.email:
            messages.info(request, 'Nie dokonano żadnych zmian')
            return redirect('user_settings')

        try:
            if username:
                request.user.username = username
            if email:
                request.user.email = email

            request.user.save()
            messages.success(request, 'Pomyślnie zaktualizowano dane użytkownika')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd: {e}')

        return redirect('user_settings')

    return render(request, 'settings/user_settings.html')

def site_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'settings/site_settings.html')

def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Stare hasło jest nieprawidłowe')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'Nowe hasła nie są takie same')
            return redirect('change_password')

        if new_password == old_password:
            messages.error(request, 'Nowe hasło nie może być takie samo jak stare')
            return redirect('change_password')

        try:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Pomyślnie zmieniono hasło')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd: {e}')

        return redirect('user_settings')

    return render(request, 'settings/change_password.html')