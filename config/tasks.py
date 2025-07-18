from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


@shared_task
def send_course_update_email(user_email, course_title):
    subject = f"Обновление курса: {course_title}"
    message = f"Здравствуйте!\n\nКурс «{course_title}» был обновлён. Зайдите, чтобы ознакомиться с новыми материалами."
    send_mail(
        subject,
        message,
        "django.ak@yandex.ru",
        [user_email],
        fail_silently=False,
    )


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    count = inactive_users.update(is_active=False)
    print(f"Deactivated {count} inactive users.")
    return count
