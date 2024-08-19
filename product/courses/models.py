from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Стоимость курса'
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name='Доступность'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='subscriptions'
    )
    is_valid = models.BooleanField(
        'Доступ',
        default=False
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_subscription')
        ]

    def __str__(self):
        return f'Пользователь: {self.user.username} | Курс: {self.course.title}'


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
        unique=True
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
        unique=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='lessons'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название'
    )
    count_student = models.IntegerField(
        verbose_name='Количество студентов',
        default=0
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        related_name='groups'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(fields=['title', 'course'], name='unique_group'),
        ]

    def __str__(self):
        return f'Группа: {self.title} | Курс: {self.course.title}'


class StudentGroup(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Студент-Группа'
        verbose_name_plural = 'Студенты-Группы'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(fields=['group', 'user'], name='unique_student_group'),
        ]

    def __str__(self):
        return (f'Группа: {self.group.title} | Студент: {self.user.username} '
                f'| Курс: {self.group.course.title}')
