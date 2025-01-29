from django.shortcuts import render

from .models import Offer
from .choices import STATE_CHOICES, TYPE_CHOICES

# Create your views here.

def main(request):
    offers = Offer.objects.all().order_by('-TimeCreated')

    type_filter = request.GET.get('type')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    state_filter = request.GET.get('state')

    if type_filter:
        offers = offers.filter(Type=type_filter)
    if price_min:
        offers = offers.filter(Price__gte=price_min)
    if price_max:
        offers = offers.filter(Price__lte=price_max)
    if state_filter:
        offers = offers.filter(State=state_filter)
    return render(request, 'core/main.html', {
        'offers': offers,
        'state_choices': STATE_CHOICES,
        'type_choices': TYPE_CHOICES,
    })