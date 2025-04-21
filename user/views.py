from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import ValidationError
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

from authentication.models import CustomUser, Review
from core.models import Offer, ApplicationForOffer
from core.choices import TYPE_CHOICES, STATE_CHOICES

def my_offers(request):
    if not request.user.is_authenticated:
        return redirect('login')

    status = request.GET.get('status', None)
    if status is None:
        user_offers = request.user.offers.all()
    elif status == 'Active':
        user_offers = request.user.offers.filter(Status='active')
    elif status == 'Closed':
        user_offers = request.user.offers.filter(Status='closed')
    elif status == 'Banned':
        user_offers = request.user.offers.filter(Status='blocked')
    else:
        messages.error(request, 'Nieprawidłowy status.')
        return redirect('user_offers')

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
            error_messages = [msg for sublist in e.message_dict.values() for msg in sublist]
            for error in error_messages:
                messages.error(request, error)
            return redirect('add_offer')

        except ValueError:
            messages.error(request, 'Nieprawidłowa cena.')
            return redirect('add_offer')

        messages.success(request, 'Oferta została dodana')
        return redirect('user_offers')

    return render(request, 'user/add_offer.html', {
        'type_choices': TYPE_CHOICES,
        'state_choices': STATE_CHOICES,
    })

def edit_specific_offer(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('login')

    offer = get_object_or_404(Offer, pk=offer_id, Status='active', Owner=request.user)

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
            return redirect('user_edit_specific_offer', offer_id=offer_id)


        try:
            price = float(price)
            expiry_date = expiry_date + ' 23:59:59'
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d %H:%M:%S')
            expiry_date = timezone.make_aware(expiry_date, timezone.get_current_timezone())

            offer.Title = title
            offer.Description = description
            offer.Price = price
            offer.ExpiryDate = expiry_date
            offer.Location = location
            offer.State = state
            offer.Type = offer_type
            offer.save()

            messages.success(request, 'Oferta została zaktualizowana')
            return redirect('user_offers')

        except ValueError as e:
            print(e)
            messages.error(request, 'Nieprawidłowa cena.')
            return redirect('user_edit_specific_offer', offer_id=offer_id)

        except ValidationError as e:
            error_messages = [msg for sublist in e.message_dict.values() for msg in sublist]
            for error in error_messages:
                messages.error(request, error)
            return redirect('user_edit_specific_offer', offer_id=offer_id)

    return render(request, 'user/edit_specific_offer.html', {
        'offer': offer,
        'state_choices': STATE_CHOICES,
        'type_choices': TYPE_CHOICES,
    })

def choose_applicants(request, offer_id):
    if not request.user.is_authenticated:
        return redirect('login')

    offer = get_object_or_404(Offer, pk=offer_id, Owner=request.user)
    applicants = ApplicationForOffer.objects.filter(offer=offer).select_related('user')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)
        if offer.chosen_user:
            messages.error(request, 'Już wybrano kandydata.')
            return redirect('user_offers')
        if user not in [app.user for app in applicants]:
            messages.error(request, 'Nie można wybrać tego kandydata.')
            return redirect('user_offers')
        if user == offer.chosen_user:
            messages.error(request, 'Ten kandydat został już wybrany.')
            return redirect('user_offers')
        try:
            offer.chosen_user = user
            offer.save()
        except ValidationError as e:
            error_messages = [msg for sublist in e.message_dict.values() for msg in sublist]
            for error in error_messages:
                messages.error(request, error)
            return redirect('user_offers')
        messages.success(request, 'Wybrano kandydata.')
        return redirect('user_offers')

    return render(request, 'user/applicants_list.html', {'applicants': applicants, 'offer': offer})

def user_applications(request):
    if not request.user.is_authenticated:
        return redirect('login')

    offers = Offer.objects.filter(offer_applications__user=request.user).distinct()

    return render(request, 'user/user_applications.html', {'offers': offers})

def submit_review(request, user_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        user = get_object_or_404(CustomUser, pk=user_id)

        try:
            Review.objects.create(
                reviewer=request.user,
                user=user,
                rating=rating,
                review=comment
            )
            messages.success(request, 'Ocena została przesłana.')

        except ValidationError as e:
            for error in e.error_list:
                messages.error(request, error.message)

    return redirect('user_offers')