from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone

from .choices import TYPE_CHOICES, STATUS_CHOICES, STATE_CHOICES

# Create your models here.
class Offer(models.Model):

    Title = models.CharField(max_length=128)
    Description = models.TextField(blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    TimeCreated = models.DateTimeField(auto_now_add=True)
    Type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='other')
    ExpiryDate = models.DateTimeField()
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    Location = models.CharField(max_length=256)
    State = models.CharField(max_length=20, choices=STATE_CHOICES)

    def clean(self):
        super().clean()
        if self.Price is None or self.Price <= 0:
            raise ValidationError({'Price': 'Cena musi być większa od zera.'})
        if self.ExpiryDate <= timezone.now():
            raise ValidationError({'ExpiryDate': 'Data wygaśnięcia musi być w przyszłości.'})
        if not self.Title:
            raise ValidationError({'Title': 'Tytuł nie może być pusty.'})
        if len(self.Title) > 128:
            raise ValidationError({'Title': 'Tytuł nie może przekraczać 128 znaków.'})
        if not self.Location:
            raise ValidationError({'Location': 'Lokalizacja nie może być pusta.'})
        if len(self.Location) > 256:
            raise ValidationError({'Location': 'Lokalizacja nie może przekraczać 256 znaków.'})
        if self.Type not in dict(TYPE_CHOICES):
            raise ValidationError({'Type': 'Nieprawidłowy typ.'})
        if self.Status not in dict(STATUS_CHOICES):
            raise ValidationError({'Status': 'Nieprawidłowy status.'})
        if self.State not in dict(STATE_CHOICES):
            raise ValidationError({'State': 'Nieprawidłowy stan.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class ApplicationForOffer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_applications')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='offer_applications')
    application_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'offer')

class OfferReport(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='offer_reports')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_offer_reports')
    reason = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'offer')

    def clean(self):
        super().clean()
        if not self.reason:
            raise ValidationError({'reason': 'Powód nie może być pusty.'})
        if len(self.reason) > 256:
            raise ValidationError({'reason': 'Powód nie może przekraczać 256 znaków.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)