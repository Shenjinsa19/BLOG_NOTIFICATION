from celery import shared_task

@shared_task
def test_task():
    print("Test task is working")
    return "Done"


from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings




# @shared_task
# def send_user_activity_summary():
#     users = User.objects.all()
#     for user in users:
#         send_mail(
#             'Your Activity Summary',
#             'Here’s what you did this week!',
#             settings.DEFAULT_FROM_EMAIL,
#             [user.email],
#             fail_silently=False,
#         )
#         print(f"✅ Sent summary to {user.email}") 
#     return "Activity summary sent"

from django.utils import timezone
from datetime import timedelta

@shared_task
def send_user_activity_summary():
    users = User.objects.all()
    now = timezone.now()

    for user in users:
        # Skip if summary was sent in last 24 hours (or 7 days, etc.)
        if user.last_summary_sent and now - user.last_summary_sent < timedelta(days=1):
            continue

        send_mail(
            'Your Activity Summary',
            'Here’s what you did this week!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        user.last_summary_sent = now
        user.save()
        print(f"✅ Sent summary to {user.email}")

    return "Activity summary sent"
