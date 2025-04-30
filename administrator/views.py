from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from authentication.models import CustomUser
from core.models import Offer, OfferReport


def users_with_low_reviews(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = CustomUser.objects.all().annotate(avg_rating=Coalesce(Avg('user__rating'), Value(0.0))).filter(avg_rating__lt=3).exclude(avg_rating=0).order_by('avg_rating')

    return render(request, 'administrator/users_with_low_reviews.html', {"users": users})

def user_statistics(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    query = request.GET.get('query', '').strip()
    user = None
    stats = {}

    if query:
        try:
            try:
                query = int(query)
                CustomUser.objects.filter(id=query)
            except ValueError:
                user = CustomUser.objects.filter(username=query)
            if not user:
                user = CustomUser.objects.filter(username__icontains=query)
        except ValueError:
            messages.error(request, "Nieprawidowy id albo nazwa użytkownika")

        if user:
            user = user.first()
            stats = {
                "date_joined": user.date_joined,
                "total_offers": Offer.objects.filter(Owner=user).count(),
                "active_offers": Offer.objects.filter(Owner=user, Status='active').count(),
                "closed_offers": Offer.objects.filter(Owner=user, Status='closed').count(),
                "avg_rating": user.get_avg_rating(),
            }
    return render(request, 'administrator/user_statistics.html', {"cur_user": user, "stats": stats})

def reported_offers(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    reported_offers = OfferReport.objects.select_related('offer', 'offer__Owner').all().filter(offer__Status='active').order_by('-report_date')

    if request.method == 'POST':
        action = request.POST.get('action')
        offer_id = request.POST.get('offer_id')
        offer = get_object_or_404(Offer, id=offer_id)

        if action == 'ban':
            offer_reports = OfferReport.objects.filter(offer=offer)
            offer_reports.delete()
            offer.Status = 'blocked'
            offer.save(skip_clean=True)
        elif action == 'ok':
            offer_reports = OfferReport.objects.filter(offer=offer)
            offer_reports.delete()
            offer.Status = 'active'
            offer.save(skip_clean=True)

    return render(request, 'administrator/reported_offers.html', {"reported_offers": reported_offers})