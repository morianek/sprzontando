from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import Avg


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(unique=True, max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avg_rating(self):
        reviews = Review.objects.filter(user=self)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return round(avg_rating, 2)
        return 0

    def __str__(self):
        return self.email

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviewer')
    review = models.TextField(max_length=500)
    rating = models.IntegerField()
    TimeCreated = models.DateTimeField(auto_now_add=True)

    def clean(self):
        self.rating = int(self.rating)
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Ocena musi być z zakresu 1-5')
        if self.user == self.reviewer:
            raise ValidationError('Nie możesz oceniać samego siebie')
        if self.review == "":
            raise ValidationError('Recenzja nie może być pusta')
        if Review.objects.filter(user=self.user, reviewer=self.reviewer).exists():
            raise ValidationError('Możesz wystawić tylko jedną recenzję dla tego użytkownika')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email