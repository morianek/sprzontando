from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Offer(models.Model):
    TYPE_CHOICES = [
        ('auto', 'Samochód'),
        ('house', 'Cały dom'),
        ('vacuum', 'odkurzanie'),
        ('sweep_mop', 'Zamiatanie i mycie podłóg'),
        ('other', 'Inne'),
    ]

    STATUS_CHOICES = [
        ('blocked', 'Zablokwane'),
        ('active', 'Aktywne'),
        ('closed', 'Zakończone'),
    ]

    Title = models.CharField(max_length=128)
    Description = models.TextField(blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')
    TimeCreated = models.DateTimeField(auto_now_add=True)
    Type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='other')
    ExpiryDate = models.DateTimeField()
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    Location = models.CharField(max_length=256)

    def clean(self):
        super().clean()
        if self.Price is None or self.Price <= 0:
            raise ValidationError({'Price': 'Cena musi być większa od zera.'})
        if self.ExpiryDate <= timezone.now():
            raise ValidationError({'ExpiryDate': 'Data wygaśnięcia musi być w przyszłości.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)