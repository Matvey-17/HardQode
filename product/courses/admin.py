from django.contrib import admin
from courses.models import Group, StudentGroup, Subscription, Course, Lesson

admin.site.register(Group)
admin.site.register(StudentGroup)
admin.site.register(Subscription)
admin.site.register(Course)
admin.site.register(Lesson)
