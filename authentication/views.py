from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def login(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('main')
    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        print(request.POST)
        return redirect('main')
    return render(request, 'authentication/register.html')

def log_out(request):
    logout(request)
    return redirect('main')