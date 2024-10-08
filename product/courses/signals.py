from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from courses.models import Subscription
from .models import Group, StudentGroup


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    if created:
        groups = Group.objects.filter(course=instance.course).order_by('count_student')

        if not groups:
            new_group = Group.objects.create(title='Группа 1', count_student=1, course=instance.course)
            StudentGroup.objects.create(group=new_group, user=instance.user)
        else:
            group = groups.first()
            if group.count_student == 0 or groups.count() >= 10:
                StudentGroup.objects.create(group=group, user=instance.user)
                group.count_student = F('count_student') + 1
                group.save()
            else:
                new_group = Group.objects.create(
                    title=f'Группа {groups.count() + 1}',
                    count_student=1,
                    course=instance.course
                )
                StudentGroup.objects.create(group=new_group, user=instance.user)

    if not instance.is_valid:
        student_group = StudentGroup.objects.filter(
            user=instance.user,
            group__course=instance.course
        ).select_related('group').first()

        if student_group:
            group = student_group.group

            if group.count_student > 0:
                group.count_student -= 1
                group.save()

            student_group.delete()
