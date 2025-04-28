import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sprzontando.settings')
django.setup()

from django.utils import timezone
from authentication.models import CustomUser


logger = logging.getLogger(__name__)

def unban_users():
    now = timezone.now()
    users = CustomUser.objects.all().exclude(ban_until=None)
    logger.info(f"Checking {users.count()} users for unban.")
    for user in users:
        try:
            if user.ban_until < now:
                user.ban_until = None
                user.is_active = True
                user.save()
                logger.info(f"Unbanned user {user.email}.")
        except Exception as e:
            logger.error(f"Failed to unban user {user.email}: {e}")

if __name__ == "__main__":
    unban_users()