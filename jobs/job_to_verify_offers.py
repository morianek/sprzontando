import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sprzontando.settings')
django.setup()

from django.utils import timezone
from core.models import Offer


logger = logging.getLogger(__name__)

def update_offers():
    now = timezone.now()
    offers = Offer.objects.filter(Status='active', ExpiryDate__lt=now)
    logger.info(f"Found {offers.count()} offers to update.")
    for offer in offers:
        try:
            offer.Status = 'closed'
            offer.save(skip_clean=True)
            logger.info(f"Updated offer {offer.id} to closed.")
        except Exception as e:
            logger.error(f"Failed to update offer {offer.id}: {e}")

if __name__ == "__main__":
    update_offers()