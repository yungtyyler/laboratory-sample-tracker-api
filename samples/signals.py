from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

# This signal creates a Token for a new user right after they are saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance:
        Token.objects.create(user=instance)
        
        try:
            send_mail(
                subject=f'New Limsly User: {instance.username}',
                message=(
                    f"A new user has just signed up for Limsly!\n\n"
                    f"Username: {instance.username}\n"
                    f"Email: {instance.email}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['tvarzeas@limsly.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending new user email: {e}")