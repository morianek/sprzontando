from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Value, Count
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.http import HttpResponseForbidden

from authentication.models import CustomUser

from .models import Offer, ApplicationForOffer, OfferReport
from .choices import STATE_CHOICES, TYPE_CHOICES

# Create your views here.

def main(request):
    offers = Offer.objects.filter(Status="active").order_by('-TimeCreated')

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
    offer = get_object_or_404(Offer, pk=offer_id, Status='active')

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
        offer = get_object_or_404(Offer, pk=offer_id, Status='active')
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

def withdraw_application(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        application = ApplicationForOffer.objects.get(offer_id=offer_id, user=request.user)
        application.delete()
        messages.success(request, 'Zgłoszenie do oferty zostało anulowane')
    except ApplicationForOffer.DoesNotExist:
        messages.error(request, 'Nie zgłosiłeś się do tej oferty')

    return redirect('specific_offer', offer_id=offer_id)

def report_offer(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if not reason:
            messages.error(request, 'Powód zgłoszenia nie może być pusty')
            return redirect('specific_offer', offer_id=offer_id)

        if OfferReport.objects.filter(offer_id=offer_id, user=request.user).exists():
            messages.error(request, 'Już zgłosiłeś tę ofertę')
            return redirect('specific_offer', offer_id=offer_id)

        offer = get_object_or_404(Offer, pk=offer_id, Status='active')

        if request.user == offer.Owner:
            messages.error(request, 'Nie możesz zgłosić swojej oferty')
            return redirect('specific_offer', offer_id=offer_id)

        try:
            OfferReport.objects.create(offer=offer, user=request.user, reason=reason)
            messages.success(request, 'Zgłoszenie zostało wysłane')
        except IntegrityError:
            messages.error(request, 'Wystąpił błąd podczas zgłaszania oferty')

    return redirect('specific_offer', offer_id=offer_id)

def ban_offer(request, offer_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden('<h1>Brak wystarczających uprawnień</h1>')

    if request.method == 'POST':
        offer = get_object_or_404(Offer, pk=offer_id, Status='active')
        try:
            offer.Status = 'blocked'
            offer.save()
            messages.success(request, 'Oferta została zbanowana')
            return redirect('main')
        except IntegrityError:
            messages.error(request, 'Wystąpił błąd podczas banowania oferty')
        except ValidationError as e:
            error_messages = [msg for sublist in e.message_dict.values() for msg in sublist]
            for error in error_messages:
                messages.error(request, error)

    return redirect('specific_offer', offer_id=offer_id)