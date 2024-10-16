from django.db import models
from django.urls import reverse
from user.models import User


class Tasks(models.Model):
    STATUS_CHOICES = [
        ('Not started', 'Не начато'),
        ('In progress', 'В процессе'),
        ('Completed', 'Выполнено'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Not started'
    )
    due_date = models.DateField(
        verbose_name='Срок выполнения',
        null=True,
        blank=True
    )

    completed = models.BooleanField(
        default=False,
        verbose_name='Завершена'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    time_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )

    time_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    objects = models.Manager()

    class Meta:
        ordering = ('-time_created',)
        indexes = [models.Index(fields=['-time_created'])]
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tasks:tasks')
