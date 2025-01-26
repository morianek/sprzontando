from django.contrib import admin
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'Owner')
    search_fields = ('Title', 'Description')
    list_filter = ('Owner',)

admin.site.register(Offer, OfferAdmin)