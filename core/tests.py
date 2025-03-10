from django.test import TestCase
from django.utils import timezone

from authentication.models import CustomUser
from core.models import ApplicationForOffer, Offer, OfferReport


# Create your tests here.

class TestModels(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email='testuser@example.com',
            password='password123'
        )
        self.offer = Offer.objects.create(
            Title='Test',
            Description='Test',
            Price=10.0,
            Owner=self.user,
            ExpiryDate=timezone.now() + timezone.timedelta(days=1),
            Location='Test',
            State='opolskie',
            Type='other'
        )

    def test_offer_model(self):
        self.assertEqual(str(self.offer), self.offer.Title)

    def test_application_for_offer_model(self):
        application = ApplicationForOffer.objects.create(
            user=self.user,
            offer=self.offer
        )
        self.assertEqual(str(application), application.user.email)

    def test_offer_report_model(self):
        report = OfferReport.objects.create(
            offer=self.offer,
            user=self.user,
            reason='Test'
        )
        self.assertEqual(str(report), report.user.email)