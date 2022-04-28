import logging

from django.core.mail import send_mail
from django.conf import settings


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
