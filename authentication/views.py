from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def login(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse('Login')
    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse('Register')
    return render(request, 'authentication/register.html')