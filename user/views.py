from django.shortcuts import render, redirect
from django.core.validators import ValidationError
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


from core.models import Offer
from core.choices import TYPE_CHOICES, STATE_CHOICES

def my_offers(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_offers = request.user.offers.all()

    return render(request, 'user/offers.html', {'offers': user_offers})


def add_offer(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        expiry_date = request.POST.get('expiry_date')
        location = request.POST.get('location')
        state = request.POST.get('state')
        offer_type = request.POST.get('type')

        if not title or not price or not expiry_date or not location or not state or not offer_type:
            messages.error(request, 'Wszystkie pola są wymagane poza opisem.')
            return redirect('add_offer')

        try:
            price = float(price)
            expiry_date = expiry_date + ' 23:59:59'
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
            expiry_date = timezone.make_aware(expiry_date, timezone.get_current_timezone())

            offer = Offer.objects.create(
                Title=title,
                Description=description,
                Price=price,
                Owner=request.user,
                ExpiryDate=expiry_date,
                Location=location,
                State=state,
                Type=offer_type,
            )
            offer.save()

        except ValidationError as e:
            error_messages = [msg for sublist in e.message_dict.values() for msg in sublist][0]
            messages.error(request, error_messages)
            return redirect('add_offer')

        except ValueError:
            messages.error(request, 'Nieprawidłowa cena.')
            return redirect('add_offer')

        messages.success(request, 'Oferta została dodana')
        return redirect('user_offers')

    return render(request, 'user/add_offer.html', {'type_choices': TYPE_CHOICES, 'state_choices': STATE_CHOICES,})