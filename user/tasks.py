from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
import logging
from django.utils import timezone
from user.models import User


# Логирование
logger = logging.getLogger(__name__)

@shared_task
def send_verification_email(email, verification_code):
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {verification_code}."
    from_email = 'blossomblessed9@gmail.com'
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Verification email sent to {email}")
    except BadHeaderError:
        logger.error(f"Invalid header found when sending email to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}. Error: {e}")

@shared_task
def send_task_reminder_emails():
    today=timezone.now().date()
    users_with_tasks=User.objects.prefetch_related('tasks').filter(
        tasks__due_date=today,
        tasks__status="Not started"
    ).distinct()

    for user in users_with_tasks:
        tasks_today=user.tasks.filter(due_date=today,status="Not started", completed=False)
        if tasks_today.exists():
            task_list="\n".join([task.name for task in tasks_today])
            message = f"Привет, {user.first_name}!\n\nНе забудь выполнить свои задачи на сегодня:\n\n{task_list}"
            send_mail(
                'Напоминание о задачах на сегодня',
                message,
                'blossomblessed9@gmail.com',
                [User.email],
                fail_silently=False,
            )


