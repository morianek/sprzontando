from django.db import models
from authentication.models import CustomUser
from django.core.exceptions import ValidationError

# Create your models here.
class Offer(models.Model):
    Title = models.CharField(max_length=128)
    Description = models.TextField(blank=True)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    Owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='offers')

    def clean(self):
        super().clean()
        if self.Price <= 0:
            raise ValidationError({'Price': 'Price must be a positive number.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)