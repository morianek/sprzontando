from django.contrib import admin
from .models import Offer, ApplicationForOffer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'Owner', 'TimeCreated')
    search_fields = ('Title', 'Description')
    list_filter = ('Owner',)

class ApplicationForOfferAdmin(admin.ModelAdmin):
    list_display = ('user', 'offer', 'application_date')
    search_fields = ('user', 'offer')
    list_filter = ('user', 'offer')

admin.site.register(Offer, OfferAdmin)
admin.site.register(ApplicationForOffer,  ApplicationForOfferAdmin)