from django.db.models.signals import post_save
from users.models import CustomUser, Balance
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def post_save_balance(sender, instance: CustomUser, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
