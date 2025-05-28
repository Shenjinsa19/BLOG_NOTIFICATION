# blogs/signals.py

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Post, Follow


# --- USER LOGIN / LOGOUT / REGISTER SIGNALS --- #

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    print(f"User logged in: {user.username}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    print(f"User logged out: {user.username}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, **kwargs):
    print(f"Login failed for: {credentials.get('username')}")

@receiver(pre_save, sender=User)
def before_user_save(sender, instance, **kwargs):
    print(f"Before saving User: {instance.username}")

@receiver(post_save, sender=User)
def after_user_save(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to My Blog',
            f'Hi {instance.username}, thank you for registering!',
            'admin@myblog.com',
            [instance.email],
            fail_silently=True,
        )
        print(f"Welcome email sent to {instance.email}")


# --- FOLLOW / UNFOLLOW SIGNALS --- #

@receiver(pre_save, sender=Follow)
def before_follow_save(sender, instance, **kwargs):
    print(f"About to save follow: {instance.follower} - {instance.author}")

@receiver(post_save, sender=Follow)
def after_follow_save(sender, instance, created, **kwargs):
    if created:
        print(f"{instance.follower.username} followed {instance.author.username}")

@receiver(pre_delete, sender=Follow)
def before_follow_delete(sender, instance, **kwargs):
    print(f"About to delete follow: {instance.follower} - {instance.author}")

@receiver(post_delete, sender=Follow)
def after_follow_delete(sender, instance, **kwargs):
    print(f"{instance.follower.username} unfollowed {instance.author.username}")


# --- POST CREATE / EDIT / DELETE SIGNALS --- #

@receiver(pre_save, sender=Post)
def before_post_save(sender, instance, **kwargs):
    print(f"About to save post titled: {instance.title} by {instance.author.username}")

@receiver(post_save, sender=Post)
def after_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Post created: {instance.title} by {instance.author.username}")
    else:
        print(f"Post edited: {instance.title} by {instance.author.username}")

@receiver(pre_delete, sender=Post)
def before_post_delete(sender, instance, **kwargs):
    print(f"About to delete post: {instance.title} by {instance.author.username}")

@receiver(post_delete, sender=Post)
def after_post_delete(sender, instance, **kwargs):
    print(f"Post deleted: {instance.title} by {instance.author.username}")
