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
    orderinfosset = {'orderinfos': ['order', 'company_name', 'website_url']}
    try:
        model.objects.create(
            title='General',
            orderinfos=orderinfosset,
            data={},
            created_by=user,
            is_service=True,
            is_default=True,
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


def _update_filters_in_session(request):
    if request.GET.get("select_package", False):
        request.session['select_package'] = list(
            map(int, request.GET.getlist("select_package"))
        )
    else:
        request.session['select_package'] = []

    if request.GET.get("select_addon", False):
        request.session['select_addon'] = list(
            map(int, request.GET.getlist("select_addon"))
        )
    else:
        request.session['select_addon'] = []

    if request.GET.get("select_status", False):
        request.session['select_status'] = list(
            map(int, request.GET.getlist("select_status"))
        )
    else:
        request.session['select_status'] = []
    
    if request.GET.get("select_user", False):
        request.session['select_user'] = list(
            map(int, request.GET.getlist("select_user"))
        )
    else:
        request.session['select_user'] = []
    
    if request.GET.get("month", False):
        request.session['month'] = int(request.GET.get("month"))
    else:
        request.session['month'] = []

    if request.GET.get("show_archived", False):
        request.session['show_archived'] = True
    else:
        request.session['show_archived'] = False


def _clear_filters_in_session(request):
    request.session['select_package'] = None
    request.session['select_addon'] = None
    request.session['select_status'] = None
    request.session['select_user'] = None
    request.session['month'] = None
    request.session['show_archived'] = None


def _get_filters_from_session(request):
    filters = {}
    if request.session.get('select_package'):
        filters["package__template_id__in"] = request.session.get('select_package')
    if request.session.get('select_addon'):
        filters["addon__template_id__in"] = request.session.get('select_addon')
    if request.session.get('select_status'):
        filters["status__in"] = request.session.get('select_status')
    if request.session.get('select_user'):
        filters["owner__in"] = request.session.get('select_user')
    if request.session.get('month'):
        filters["month"] = request.session.get('month')
    if request.session.get('show_archived'):
        filters["is_archived"] = request.session.get('show_archived')

    if not filters.get('owner__in') and not request.user.is_client:
        user_ids = []
        user_ids.append(request.user.id)
        for client in request.user.client.all():
            user_ids.append(client.id)
        if user_ids:
            filters['owner__in'] = user_ids

    return filters
