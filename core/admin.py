from django.contrib import admin
from .models import Offer, Review

class OfferAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Description', 'Owner', 'TimeCreated')
    search_fields = ('Title', 'Description')
    list_filter = ('Owner',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('Rating', 'Description', 'Reviewer', 'TimeCreated', 'Offer')
    search_fields = ('Description',)
    list_filter = ('Reviewer', 'Offer')

admin.site.register(Offer, OfferAdmin)
admin.site.register(Review, ReviewAdmin)