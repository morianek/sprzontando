from django.shortcuts import render, redirect

# Create your views here.

def my_offers(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_offers = request.user.offers.all()
    print(user_offers)
    return render(request, 'user/offers.html', {'offers': user_offers})