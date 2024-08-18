from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Subscription
from .models import Group, StudentGroup


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        group = Group.objects.filter(course=instance.course).order_by('count_student').first()

        if group:
            StudentGroup.objects.create(group=group, user=instance.user)
            group.count_student = F('count_student') + 1
            group.save()
