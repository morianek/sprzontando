from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.db.models import Avg, Value, Count
from django.db.models.functions import Coalesce
from django.contrib import messages

from authentication.models import CustomUser

from .models import Offer, ApplicationForOffer
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

def ranking(request):
    best_users = CustomUser.objects.annotate(
        avg_rating=Coalesce(Avg('user__rating'), Value(0.0)),
        review_count=Count('user__rating')
    ).filter(avg_rating__gt=0).order_by('-avg_rating')[:5]

    return render(request, 'core/ranking.html', {
        'users': best_users,
    })

def specific_offer(request, offer_id):
    try:
        offer = Offer.objects.get(pk=offer_id)

    except Offer.DoesNotExist:
        messages.error(request, 'Nie znaleziono oferty o podanym ID')
        return redirect('main')

    did_user_apply = False
    if request.user.is_authenticated:
        did_user_apply = ApplicationForOffer.objects.filter(offer=offer, user=request.user).exists()

    return render(request, 'core/specific_offer.html', {
        'offer': offer,
        'did_user_apply': did_user_apply,
    })

def apply_for_offer(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        offer = Offer.objects.get(pk=offer_id)
        user = request.user

        if not user or not offer:
            messages.error(request, 'Wystąpił błąd podczas zgłaszania się do oferty')
            return redirect(specific_offer, offer_id)

        if user == offer.Owner:
            messages.error(request, 'Nie możesz zgłosić się do swojej oferty')
            return redirect(specific_offer, offer_id)

        if ApplicationForOffer.objects.filter(offer=offer, user=user).exists():
            messages.error(request, 'Już zgłosiłeś się do tej oferty')
            return redirect(specific_offer, offer_id)

        try:
            ApplicationForOffer(offer=offer, user=user).save()
            messages.success(request, 'Zgłoszenie do oferty zostało złożone')

        except IntegrityError:
            messages.error(request, 'Wystąpił błąd podczas zgłaszania się do oferty')

    return redirect(specific_offer, offer_id)