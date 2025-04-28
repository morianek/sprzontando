from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden
from django.shortcuts import render
from authentication.models import CustomUser

def users_with_low_reviews(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = CustomUser.objects.all().annotate(avg_rating=Coalesce(Avg('user__rating'), Value(0.0))).filter(avg_rating__lt=3).exclude(avg_rating=0).order_by('avg_rating')

    return render(request, 'administrator/users_with_low_reviews.html', {"users": users})