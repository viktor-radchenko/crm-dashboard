import os
import logging
import secrets

from mailjet_rest import Client

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from app_users.models import UserReplication


def send_email_to_client(subject, body, recipients):
    try:
        from_email = settings.EMAIL_HOST_USER

        send_mail(
            subject,
            body,
            from_email,
            recipients
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

def _create_intake_form(user, model):
    orderinfosset = {'orderinfos': ['order', 'company_name', 'company_address', 'company_city', 'company_state', 'company_zip', 'company_country', 'company_phone', 'website_url', 'company_email', 'company_description', 'logo_image', 'map_url', 'website_login_url', 'web_username', 'web_password', 'analytics_account']}
    try:
        model.objects.create(
            title='Intake form',
            orderinfos=orderinfosset,
            data={},
            created_by=user,
        )
    except:
        pass

def _add_notification(text, target, model, link):
    model.objects.create(
        owner=target,
        link=link,
        text=text,
    )

def send_mailjet_email(recipient, subj, body):
    try:
        api_key = os.getenv('MAILJET_API_KEY')
        api_secret = os.getenv('MAILJET_SECRET_KEY')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        data = {
        'Messages': [
            {
            "From": {
                "Email": os.getenv('MAILJET_SENDER', "viktordevtest2022@gmail.com"),
                "Name": "Viktor"
            },
            "To": [
                {
                "Email": recipient.email,
                "Name": recipient.first_name
                }
            ],
            "Subject": subj,
            "TextPart": body,
            "HTMLPart": body,
            "CustomID": "AppGettingStartedTest"
            }
        ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    except Exception as e:
        logging.error("Exception: " + str(e))