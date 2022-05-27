import logging
import secrets

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from app_users.models import UserReplication


def send_email_to_client(subject, body, recepients):
    try:
        from_email = settings.EMAIL_HOST_USER

        send_mail(
            subject,
            body,
            from_email,
            recepients
        )
    except Exception as e:
        logging.error("Exception: " + str(e))


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.is_active)
        )
account_activation_token = TokenGenerator()


def _delete_user(user):
    user.is_active = False
    user.is_deleted = True
    user.is_staff = False
    user.is_registered = False

    new_email = f'{settings.CLIENT_TAG}-{secrets.token_hex(16)}@searchmanager.pro'

    replicated_user = UserReplication(old_email=user.email, new_email=new_email, user_uuid=user.uuid, original_user=user)
    replicated_user.save()

    user.email = new_email
    user.save()


def _create_statuses(user, model):
    statuses = ["Cancelled", "New", "In progress", "Completed", "Waiting for approval", "Approved"]
    for idx, stat in enumerate(statuses):
        try:
            status = model(val=idx, name=stat, created_by=user)
            status.save()
        except:
            pass
