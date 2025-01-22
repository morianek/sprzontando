from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password'})
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