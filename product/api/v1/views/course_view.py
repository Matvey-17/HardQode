from django.db.models import Count, Avg, ExpressionWrapper, FloatField, Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course, Subscription
from users.models import Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course.objects.prefetch_related('lessons', 'subscriptions'),
                                   id=self.kwargs.get('course_id'))
        if course.subscriptions.filter(user=self.request.user):
            return course.lessons.all()

        return []


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course.objects.prefetch_related('groups'), id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.filter(is_valid=True).prefetch_related('lessons').annotate(
        lessons_count=Count('lessons', distinct=True),
        student_count=Count('subscriptions', distinct=True, filter=Q(subscriptions__is_valid=True)),
        procent_group=ExpressionWrapper(Avg('groups__count_student') / 30, output_field=FloatField()))
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        with transaction.atomic():
            balance = get_object_or_404(Balance, user=request.user)

            course = get_object_or_404(Course, id=pk)

            if course.price <= balance.balance:
                balance.balance -= course.price
                balance.save()

                subscription = Subscription.objects.select_related('user', 'course').filter(user=request.user,
                                                                                            course=course).first()

                if not subscription:
                    subscription = Subscription.objects.create(user=request.user, course=course)

                subscription.is_valid = True
                subscription.save()

                data = SubscriptionSerializer(subscription)

                return Response(
                    data=data.data,
                    status=status.HTTP_201_CREATED
                )

            return Response({'detail': 'Недостаточно средств (бонусов)'}, status.HTTP_400_BAD_REQUEST)
