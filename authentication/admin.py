from django.contrib import admin

from .models import CustomUser, Review

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'reviewer', 'rating', 'TimeCreated')
    search_fields = ('user', 'reviewer')
    list_filter = ('rating', 'TimeCreated')

admin.site.register(Review, ReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

