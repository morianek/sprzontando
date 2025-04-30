from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.validators import EmailValidator, ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import CustomUser

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Email i hasło są wymagane')
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Email lub hasło są nieprawidłowe')
            return redirect('login')

    return render(request, 'authentication/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('password2')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email jest już zajęty')
            return redirect('register')

        if CustomUser.objects.filter(username=name).exists():
            messages.error(request, 'Nazwa użytkownika jest już zajęta')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Hasła nie są takie same')
            return redirect('register')

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            messages.error(request, 'Nieprawidłowy format adresu email')
            return redirect('register')

        try:
            user = CustomUser.objects.create(
                email=email,
                username=name,
                password=make_password(password)
            )
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(f'/auth/activate/{uid}/{token}/')

            send_mail(
                'Aktywacja konta',
                f'Kliknij w link, aby aktywować konto: {activation_link}',
                'Sprzontando2001@gmail.com',
                [email],
            )
            return render(request, 'authentication/registration_pending.html')
        except Exception as e:
            messages.error(request, f'Wystąpił błąd: {e}')
            return redirect('register')

    return render(request, 'authentication/register.html')

def activate(request, uidb64, token):
    print("test")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Konto zostało aktywowane. Możesz się zalogować.')
        return redirect('login')
    else:
        return HttpResponse('Link aktywacyjny jest nieprawidłowy lub wygasł.')

def log_out(request):
    logout(request)
    return redirect('login')

def user_settings(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username == request.user.username and email == request.user.email:
            messages.info(request, 'Nie dokonano żadnych zmian')
            return redirect('user_settings')

        if CustomUser.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Nazwa użytkownika jest już zajęta')
            return redirect('user_settings')

        if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Email jest już zajęty')
            return redirect('user_settings')

        email_validator = EmailValidator()
        try:
            email_validator(email)
        except ValidationError:
            messages.error(request, 'Nieprawidłowy format adresu email')
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