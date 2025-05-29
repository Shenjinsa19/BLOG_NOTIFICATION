import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Post, Follow
logger = logging.getLogger(__name__)

# login.logout,register

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username}")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f"User logged out: {user.username}")

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, **kwargs):
    username = credentials.get('username', '<unknown>')
    logger.warning(f"Login failed for: {username}")

@receiver(pre_save, sender=User)
def before_user_save(sender, instance, **kwargs):
    logger.debug(f"Before saving User: {instance.username}")

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
        logger.info(f"Welcome email sent to {instance.email}")

# folow,unfollow

@receiver(pre_save, sender=Follow)
def before_follow_save(sender, instance, **kwargs):
    logger.debug(f"About to save follow: {instance.follower}  {instance.author}")

@receiver(post_save, sender=Follow)
def after_follow_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"{instance.follower.username} followed {instance.author.username}")

@receiver(pre_delete, sender=Follow)
def before_follow_delete(sender, instance, **kwargs):
    logger.debug(f"About to delete follow: {instance.follower}  {instance.author}")

@receiver(post_delete, sender=Follow)
def after_follow_delete(sender, instance, **kwargs):
    logger.info(f"{instance.follower.username} unfollowed {instance.author.username}")

#create,edit,delere

@receiver(pre_save, sender=Post)
def before_post_save(sender, instance, **kwargs):
    if instance.pk:
        logger.info(f"Post '{instance.title}' is about to be edited by {instance.author.username}")
    else:
        logger.info(f"Post '{instance.title}' is about to be created by {instance.author.username}")

@receiver(post_save, sender=Post)
def after_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Post created: '{instance.title}' by {instance.author.username}")
    else:
        logger.info(f"Post edited: '{instance.title}' by {instance.author.username}")

@receiver(pre_delete, sender=Post)
def before_post_delete(sender, instance, **kwargs):
    logger.info(f"Post '{instance.title}' by {instance.author.username} is about to be deleted")

@receiver(post_delete, sender=Post)
def after_post_delete(sender, instance, **kwargs):
    logger.info(f"Post '{instance.title}' by {instance.author.username} has been deleted")
