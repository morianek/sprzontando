from django.shortcuts import render

from .models import Offer

# Create your views here.

def main(request):
    offers = Offer.objects.all().order_by('-TimeCreated')
    return render(request, 'core/main.html', {'offers': offers})