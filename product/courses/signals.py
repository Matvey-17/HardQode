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
        group = Group.objects.filter(course=instance.course).order_by('count_student')

        if not group:
            new_group = Group.objects.create(title='Группа 1', count_student=1, course=instance.course)
            StudentGroup.objects.create(group=new_group, user=instance.user)

        elif group.first().count_student == 0:
            StudentGroup.objects.create(group=group.first(), user=instance.user)
            group.first().count_student = 1
            group.first().save()

        elif group.count() < 10:
            new_group = Group.objects.create(title=f'Группа {group.count() + 1}', count_student=1,
                                             course=instance.course)
            StudentGroup.objects.create(group=new_group, user=instance.user)

        else:
            StudentGroup.objects.create(group=group.first(), user=instance.user)
            group.count_student = F('count_student') + 1
            group.save()