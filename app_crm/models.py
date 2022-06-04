import logging
import re
import secrets
from turtle import back
from xml.dom.expatbuilder import Rejecter

import requests
import json

from django.db import models
from django.core.exceptions import ValidationError
from django.core import serializers
from app_users.models import CustomUser, UserReplication
from django.contrib import auth, messages
from django.conf import settings

from app_crm.utils import (
    account_activation_token,
    _delete_user,
    _create_statuses,
    _create_intake_form,
    _add_notification,
    send_mailjet_email,
    _update_filters_in_session,
    _get_filters_from_session
)

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


# Create your models here.


class Order(models.Model):
    order = models.CharField(max_length=500)
    company_name = models.CharField(max_length=5000)
    company_address = models.CharField(max_length=5000)
    company_city = models.CharField(max_length=5000)
    company_state = models.CharField(max_length=5000)
    company_zip = models.CharField(max_length=5000)
    company_country = models.CharField(max_length=5000)
    company_phone = models.CharField(max_length=5000)
    website_url = models.CharField(max_length=5000)
    company_email = models.CharField(max_length=5000)
    company_description = models.CharField(max_length=5000)
    logo_image = models.CharField(max_length=5000)
    map_url = models.CharField(max_length=5000)
    website_login_url = models.CharField(max_length=5000)
    web_username = models.CharField(max_length=5000)
    web_password = models.CharField(max_length=5000)
    analytics_account = models.CharField(max_length=5000)

    link1 = models.CharField(max_length=10000)
    link2 = models.CharField(max_length=10000)
    link3 = models.CharField(max_length=10000)
    link4 = models.CharField(max_length=10000)
    note = models.TextField()
    start_date = models.DateField(default=None, blank=True, null=True)
    renewal_date = models.DateField(default=None, blank=True, null=True)
    status = models.ForeignKey(
        "Status", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None
    )

    extra_fields = models.JSONField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True,
        default=None,
        related_name="order",
    )
    month = models.IntegerField(default=None, blank=True)
    package = models.ForeignKey(
        "Package", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None
    )
    addon = models.ManyToManyField("Addon", blank=True, default=None)

    def __str__(self):
        return self.order

    def getOrderById(request, id):
        order = Order.objects.get(id=id)
        if not order:
            return False
        if order.owner == request.user or order.owner.created_by == request.user:
            return order
        else:
            return False

    def createCustomOrder(request):
        order_num = re.sub("\D", "", request.POST["order"])
        client_selected = request.POST.get("userid", None)
        if not client_selected:
            return False, "You need to add a client first"
        userid = CustomUser.objects.get(id=request.POST["userid"])

        formid = request.POST.get("service_form_id")
        form = Form.objects.get(id=formid)

        # create statuses:
        stat = request.user.status.filter(val=1).first()

        # create dict from additional fields
        extra_fields = {}
        for formfieldnum in form.data:
            formfield = form.data.get(formfieldnum)
            title = formfield.get("title")
            if formfield.get("type") == 1:
                extra_fields[title] = request.POST.getlist(str(form.id) + ":" + str(formfieldnum))
            else:
                extra_fields[title] = request.POST.get(str(form.id) + ":" + str(formfieldnum))

        order_notes = request.POST.get("notes")

        new_order = Order(
            order=order_num,
            company_name=request.POST.get("company_name", ""),
            company_address=request.POST.get("company_address", ""),
            company_city=request.POST.get("company_city", ""),
            company_state=request.POST.get("company_state", ""),
            company_zip=request.POST.get("company_zip", ""),
            company_country=request.POST.get("company_country", ""),
            company_phone=request.POST.get("company_phone", ""),
            website_url=request.POST.get("website_url", ""),
            company_email=request.POST.get("company_email", ""),
            company_description=request.POST.get("company_description", ""),
            logo_image=request.POST.get("logo_image", ""),
            map_url=request.POST.get("map_url", ""),
            website_login_url=request.POST.get("website_login_url", ""),
            web_username=request.POST.get("web_username", ""),
            web_password=request.POST.get("web_password", ""),
            analytics_account=request.POST.get("analytics_account", ""),
            start_date=None,
            renewal_date=None,
            status=stat,
            owner=userid,
            month=1,
            extra_fields=extra_fields,
            notes=order_notes,
        )
        new_order.save()
        form.order = new_order
        form.save()
        return True, "Order successfully created"

    def deleteOrder(id):
        order = Order.objects.get(id=id)
        if order.package != None:
            package = order.package
            tasks = package.tasks.all()
            tasks.delete()
            package.delete()
        order.delete()

    def editInfo(request, id):
        order = Order.objects.get(id=id)
        if not order and (
            order.owner != request.user or order.owner.created_by != request.user
        ):
            return
        # process form fields
        form = order.intake_form.first()
        extra_fields = {}
        for formfieldnum in form.data:
            formfield = form.data.get(formfieldnum)
            title = formfield.get("title")
            if formfield.get("type") == 1:
                extra_fields[title] = request.POST.getlist(str(form.id) + ":" + str(formfieldnum))
            else:
                extra_fields[title] = request.POST.get(str(form.id) + ":" + str(formfieldnum))
        order_notes = request.POST.get("notes")

        order.order = re.sub("\D", "", request.POST["order"])
        order.company_name = request.POST.get("company_name", "")
        order.company_address = request.POST.get("company_address", "")
        order.company_city = request.POST.get("company_city", "")
        order.company_state = request.POST.get("company_state", "")
        order.company_zip = request.POST.get("company_zip", "")
        order.company_country = request.POST.get("company_country", "")
        order.company_phone = request.POST.get("company_phone", "")
        order.website_url = request.POST.get("website_url", "")
        order.company_email = request.POST.get("company_email", "")
        order.company_description = request.POST.get("company_description", "")
        order.logo_image = request.POST.get("logo_image", "")
        order.map_url = request.POST.get("map_url", "")
        order.website_login_url = request.POST.get("website_login_url", "")
        order.web_username = request.POST.get("web_username", "")
        order.web_password = request.POST.get("web_password", "")
        order.analytics_account = request.POST.get("analytics_account", "")
        order.extra_fields = extra_fields
        order.notes = order_notes
        order.save()

    def editOrder(request, id):
        order = Order.objects.get(id=id)
        if not order and (
            order.owner != request.user or order.owner.created_by != request.user
        ):
            return
        order.link1 = request.POST["link1"]
        order.link2 = request.POST["link2"]
        order.link3 = request.POST["link3"]
        order.link4 = request.POST["link4"]
        order.note = request.POST["note"]
        if int(request.POST["own"]) != order.owner.id:
            order.owner = CustomUser.objects.get(id=int(request.POST["own"]))
        if not request.POST["start_date"]:
            order.start_date = None
        else:
            order.start_date = request.POST["start_date"]
        if not request.POST["renewal_date"]:
            order.renewal_date = None
        else:
            order.renewal_date = request.POST["renewal_date"]
        order.status = Status.objects.get(id=int(request.POST["status"]))
        old_month = order.month
        order.month = int(request.POST["month"])
        new_month = order.month
        pack = request.POST["package"]

        try:
            pack = int(pack)
        except ValueError:
            pass

        if order.package == None and pack != "None":
            tPackage = templatePackage.objects.get(id=pack)
            task_ids = []
            tasks = []
            for mon in tPackage.month.all():
                for ta in mon.orderby_set.all():
                    tasks.append(
                        Task(
                            start_date=None,
                            end_date=None,
                            completed_by=None,
                            status=None,
                            notes="",
                            report_link="",
                            month=mon.num,
                            template_task=ta.templateTask,
                            ordering=ta.ordering,
                        )
                    )

            tSave = Task.objects.bulk_create(tasks)
            for obj in tSave:
                task_ids.append(obj.id)
            package = Package.objects.create(template=tPackage)
            package.tasks.set(task_ids)
            order.package = package
        elif order.package != None and pack == "None":
            order.package.tasks.all().delete()
            order.package.delete()
            order.package = None

        order.save()

        str_template_addon = request.POST.getlist("addon")
        int_template_addon = []
        for _ in str_template_addon:
            try:
                int_template_addon.append(int(_))
            except:
                pass

        addons = order.addon.all()
        addons_ids = [x.template.id for x in addons]

        if new_month == old_month:
            pass
        elif new_month < old_month:
            for addon in addons:
                for addontask in addon.tasks.all():
                    if addontask.month > new_month:
                        addontask.delete()
        elif new_month > old_month:
            for addon in addons:
                temp = addon.template.addonorderby_set.all()
                newTasks = []
                for x in range(old_month + 1, new_month + 1):
                    for t in temp:
                        newTasks.append(
                            Task(
                                start_date=None,
                                status=None,
                                month=x,
                                end_date=None,
                                completed_by=None,
                                notes="",
                                report_link="",
                                template_task=t.templateTask,
                                ordering=t.ordering,
                            )
                        )
                toSave = Task.objects.bulk_create(newTasks)
                for obj in toSave:
                    addon.tasks.add(obj)

        addons = order.addon.all()
        addons_ids = [x.template.id for x in addons]

        if int_template_addon:
            for addon in addons:
                if addon.template.id not in int_template_addon:
                    addon.tasks.all().delete()
                    addon.delete()
            for addonid in int_template_addon:
                if addonid not in addons_ids:
                    getTemplateAddon = templateAddon.objects.get(id=addonid)
                    getTemplateTasks = getTemplateAddon.addonorderby_set.all()
                    newTasks = []
                    for x in range(1, order.month + 1):
                        for templateAddonTask in getTemplateTasks:
                            newTasks.append(
                                Task(
                                    start_date=None,
                                    status=None,
                                    month=x,
                                    end_date=None,
                                    completed_by=None,
                                    notes="",
                                    report_link="",
                                    template_task=templateAddonTask.templateTask,
                                    ordering=templateAddonTask.ordering,
                                )
                            )
                    toSave = Task.objects.bulk_create(newTasks)
                    newTasksIds = []
                    for obj in toSave:
                        newTasksIds.append(obj.id)
                    newAddon = Addon.objects.create(template=getTemplateAddon)
                    newAddon.tasks.set(newTasksIds)
                    order.addon.add(newAddon)
        else:
            if addons:
                for orderAddon in addons:
                    orderAddon.tasks.all().delete()
                    orderAddon.delete()

    def cancelOrder(id):
        order = Order.objects.get(id=id)
        order.is_archived = True
        order.save()

    def getAllOrders(request):
        filters = _get_filters_from_session(request)
        orders = Order.objects.filter(**filters).exclude(
            owner__is_deleted=True
        )
        return orders

    def createUserOrder(request):
        order_num = re.sub("\D", "", request.POST["order"])

        formid = request.POST.get("service_form_id")
        form = Form.objects.get(id=formid)

        stat = Status.objects.filter(val=1).first()

        extra_fields = {}
        for formfieldnum in form.data:
            formfield = form.data.get(formfieldnum)
            title = formfield.get("title")
            if formfield.get("type") == 1:
                extra_fields[title] = request.POST.getlist(str(form.id) + ":" + str(formfieldnum))
            else:
                extra_fields[title] = request.POST.get(str(form.id) + ":" + str(formfieldnum))

        order_notes = request.POST.get("notes")

        order = Order(
            order=order_num,
            company_name=request.POST.get("company_name", ""),
            company_address=request.POST.get("company_address", ""),
            company_city=request.POST.get("company_city", ""),
            company_state=request.POST.get("company_state", ""),
            company_zip=request.POST.get("company_zip", ""),
            company_country=request.POST.get("company_country", ""),
            company_phone=request.POST.get("company_phone", ""),
            website_url=request.POST.get("website_url", ""),
            company_email=request.POST.get("company_email", ""),
            company_description=request.POST.get("company_description", ""),
            logo_image=request.POST.get("logo_image", ""),
            map_url=request.POST.get("map_url", ""),
            website_login_url=request.POST.get("website_login_url", ""),
            web_username=request.POST.get("web_username", ""),
            web_password=request.POST.get("web_password", ""),
            analytics_account=request.POST.get("analytics_account", ""),
            start_date=None,
            renewal_date=None,
            status=stat,
            owner=request.user,
            month=1,
            extra_fields=extra_fields,
            notes=order_notes,
        )
        order.save()
        form.order = order
        form.save()

        text = f"Your client {request.user.first_name} has created a new order"
        link = f"/dashboard/admin/editinfo/{order.id}/"

        _add_notification(
            text, target=request.user.created_by, model=Notification, link=link
        )

        recipient = request.user.created_by
        subj = "SearManager.pro - your client has created an order"

        url = f"{request._current_scheme_host}/dashboard/admin/editinfo/{order.id}/"
        body = render_to_string(
            "email/client_create_order.html",
            {
                "recipient": recipient,
                "url": url,
                "client": request.user,
            },
        )
        send_mailjet_email(recipient, subj, body)

        return True

    def editUserOrder(request, id):
        order = Order.objects.get(id=id)

         # process form fields
        form = order.intake_form.first()
        extra_fields = {}
        for formfieldnum in form.data:
            formfield = form.data.get(formfieldnum)
            title = formfield.get("title")
            if formfield.get("type") == 1:
                extra_fields[title] = request.POST.getlist(str(form.id) + ":" + str(formfieldnum))
            else:
                extra_fields[title] = request.POST.get(str(form.id) + ":" + str(formfieldnum))
        order_notes = request.POST.get("notes")

        order.order = re.sub("\D", "", request.POST["order"])
        order.company_name = request.POST.get("company_name", "")
        order.company_address = request.POST.get("company_address", "")
        order.company_city = request.POST.get("company_city", "")
        order.company_state = request.POST.get("company_state", "")
        order.company_zip = request.POST.get("company_zip", "")
        order.company_country = request.POST.get("company_country", "")
        order.company_phone = request.POST.get("company_phone", "")
        order.website_url = request.POST.get("website_url", "")
        order.company_email = request.POST.get("company_email", "")
        order.company_description = request.POST.get("company_description", "")
        order.logo_image = request.POST.get("logo_image", "")
        order.map_url = request.POST.get("map_url", "")
        order.website_login_url = request.POST.get("website_login_url", "")
        order.web_username = request.POST.get("web_username", "")
        order.web_password = request.POST.get("web_password", "")
        order.analytics_account = request.POST.get("analytics_account", "")
        order.extra_fields = extra_fields
        order.notes = order_notes
        order.save()

    def getUserOrders(request):
        orders = Order.objects.filter(owner=request.user.id)
        return orders

    def sendMessageNotification(request, msg):
        if request.user.is_client:
            zap = request.user.created_by.key.first()
        else:
            zap = request.user.key.first()
        # check if no recipient in case client is not registered
        if not msg.recipient:
            return False
        if zap:
            dataset = dict(
                order=msg.order.order,
                name=msg.author.first_name,
                email=msg.author.email,
                company=msg.order.company_name,
                body=msg.body,
                date_added=msg.date_added.strftime("%d-%m-%Y %H:%M"),
                url=f"{request._current_scheme_host}/dashboard/chatroom/{msg.order.id}/",
                recipients=msg.recipient,
                message_type="chat_message",
            )
            try:
                r = requests.post(zap.apikey, data=json.dumps(dataset))
                return r.ok
            except:
                return False
        return False

    def getUnreadMessages(request, orders):
        recipient = request.user.email
        unread = []
        for ord in orders:
            if ord.message.filter(recipient=recipient, is_read=False):
                unread.append(ord.id)
        return unread

    def sendAllInfo(request, id):
        order = Order.objects.get(id=id)
        if order.owner.created_by != request.user:
            return False, "You don't have permission to use this API"
        
        deliv_link = (
            "https://searchmanager.pro/dashboard/admin/"
            + str(order.id)
            + "/deliverables/"
        )

        dataset = {
            "order": order.order,
            "company_name": order.company_name,
            "company_address": order.company_address,
            "company_city": order.company_city,
            "company_state": order.company_state,
            "company_zip": order.company_zip,
            "company_country": order.company_country,
            "company_phone": order.company_phone,
            "website_url": order.website_url,
            "company_email": order.company_email,
            "company_description": order.company_description,
            "logo_image": order.logo_image,
            "map_url": order.map_url,
            "website_login_url": order.website_login_url,
            "web_username": order.web_username,
            "web_password": order.web_password,
            "analytics_account": order.analytics_account,
            "deliverables_url": deliv_link,
            "message_type": "all_info",
        }

        apikey = request.user.key.first()
        if not apikey:
            try:
                recipient = order.owner
                subj = "SearchManager.pro - update on order deliverables"
                body = render_to_string(
                    "email/zap_backup.html",
                    {
                        "dataset": dataset,
                    },
                )

                send_mailjet_email(recipient, subj, body)

                return r.ok, "Data has been sent successfully"
            except Exception as e:
                logging.error("Exception: " + str(e))
                return (
                    False,
                    "We were unable to send data to Zapier. Please check you Zapier API key url is correct",
                )
        try:
            r = requests.post(apikey.apikey, data=json.dumps(dataset))
            return r.ok, "Data has been sent successfully"
        except:
            return (
                False,
                "We were unable to send data to Zapier. Please check you Zapier API key url is correct",
            )

    def sendForm(request, id, formid):
        order = Order.objects.get(id=id)
        if order.owner.created_by != request.user:
            return False, "You don't have permission to use this API"
        apikey = request.user.key.first()
        if apikey:
            form = Form.objects.get(id=formid)

            orderfields = form.orderinfos.get("orderinfos")
            formfields = form.data.get

            dataset = {}

            for orderfield in orderfields:
                dataset[orderfield] = request.POST.get(orderfield)

            for formfieldnum in form.data:
                formfield = form.data.get(formfieldnum)
                if formfield.get("type") == 1:
                    dataset[formfieldnum] = {
                        "title": formfield.get("title"),
                        "answer": request.POST.getlist(
                            str(form.id) + ":" + str(formfieldnum)
                        ),
                    }
                else:
                    dataset[formfieldnum] = {
                        "title": formfield.get("title"),
                        "answer": request.POST.get(
                            str(form.id) + ":" + str(formfieldnum)
                        ),
                    }

            dataset["form_note"] = request.POST.get("formnote")

            dataset["form_name"] = form.title
            dataset["message_type"] = "form_info"

            r = requests.post(apikey.apikey, data=json.dumps(dataset))
            return r.ok, "Form was sent successfully"
        else:
            return (
                False,
                'No Zapier API key provided. You can add one <a href="/dashboard/admin/editkey/">here</a>',
            )

    def getOrdersByFilter(request):
        _update_filters_in_session(request)
        filters = _get_filters_from_session(request)
        orders = Order.objects.filter(**filters).exclude(owner__is_deleted=True)
        return orders


class Package(models.Model):
    tasks = models.ManyToManyField("Task", blank=True, default=None)
    template = models.ForeignKey(
        "templatePackage", on_delete=models.CASCADE, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.template.title

    def getPackageById(id):
        pack = Package.objects.filter(id=id).first()
        return pack


class Task(models.Model):
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    completed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        blank=True,
        related_name="completed_by",
    )
    status = models.ForeignKey(
        "Status", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None
    )
    notes = models.TextField(default=None, blank=True)
    report_link = models.CharField(max_length=10000, blank=True)
    month = models.IntegerField(default=None, blank=True)
    template_task = models.ForeignKey("templateTask", on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __str__(self):
        return self.template_task.title

    def editTask(request, id):
        task = Task.objects.get(id=id)

        if request.POST["start_date"] == "":
            local_start_date = None
            task.start_date = local_start_date
        else:
            local_start_date = request.POST["start_date"]
            task.start_date = local_start_date

        if request.POST["end_date"] == "":
            local_end_date = None
            task.end_date = local_end_date
        else:
            local_end_date = request.POST["end_date"]
            task.end_date = local_end_date

        local_status = Status.objects.get(id=int(request.POST["status"]))
        task.status = local_status
        task.report_link = request.POST["report_link"]
        task.notes = request.POST["note"]
        task.save()

        additional = request.POST.getlist("addtasks")
        for addit in additional:
            sometask = Task.objects.filter(id=int(addit)).update(
                start_date=local_start_date,
                status=local_status,
                end_date=local_end_date,
            )

    def getTaskById(id):
        task = Task.objects.filter(id=id).first()
        return task

    def removeTask(id):
        Task.objects.filter(id=id).delete()


class templatePackage(models.Model):
    title = models.CharField(max_length=500)
    color = models.CharField(max_length=500)
    num_of_month = models.IntegerField(default=None, blank=True)
    month = models.ManyToManyField("Month", blank=True, default=None)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="temlpatePackage"
    )

    def __str__(self):
        return self.title

    def createPackage(request):
        nom = int(request.POST["month"])
        nom_list = range(1, nom + 1)
        tempPack = templatePackage.objects.create(
            title=request.POST["title"],
            color=request.POST["color"],
            num_of_month=nom,
            created_by=request.user,
        )
        month_ids = []
        for x in nom_list:
            z = Month.objects.create(num=x)
            month_ids.append(z.id)
        for y in month_ids:
            tempPack.month.add(y)
        return tempPack.id

    def getAllPackage(request):
        user = request.user
        pack = user.temlpatePackage.all()
        return pack

    def getPackageById(id):
        pack = templatePackage.objects.filter(id=id).first()
        return pack

    def editPackage(request, id):
        pack = templatePackage.objects.get(id=id)
        if not pack or pack.created_by != request.user:
            return
        pack.title = request.POST["title"]
        pack.color = request.POST["color"]
        nomn = int(request.POST["month"])
        nomo = int(pack.num_of_month)
        if nomn == nomo:
            pass
        elif nomn < nomo:
            for x in pack.month.all():
                if x.num > nomn:
                    x.delete()
            pack.num_of_month = nomn

            packages = Package.objects.filter(template=id).prefetch_related("tasks")
            for package in packages:
                for task in package.tasks.all():
                    if task.month > nomn:
                        task.delete()
        elif nomn > nomo:
            nsum = nomn - nomo
            tnomo = nomo
            for x in range(nsum):
                tnomo = tnomo + 1
                pack.month.create(num=tnomo)
                pack.num_of_month = nomn
        pack.save()

    def removePackage(request, id):
        tpack = templatePackage.objects.get(id=id)
        if not tpack or tpack.created_by != request.user:
            return
        tpack.month.all().delete()
        tpack.delete()
        package = Package.objects.filter(template=id)
        for p in package:
            p.tasks.all().delete()
        return True


class orderBy(models.Model):
    month = models.ForeignKey("Month", on_delete=models.CASCADE)
    templateTask = models.ForeignKey("templateTask", on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __str__(self):
        return self.templateTask.title


class Month(models.Model):
    num = models.IntegerField(default=None, blank=True)
    template_tasks = models.ManyToManyField(
        "templateTask", blank=True, default=None, through="orderBy"
    )

    def __str__(self):
        return "Month " + str(self.num)

    def getMonthById(id):
        m = Month.objects.get(id=id)
        return m

    def editMonth(request, pid, id):
        month = Month.objects.get(id=id)
        tasks = [x for x in request.POST.getlist("check")]

        def getOrderding(w):
            for r in tasks:
                y = r.split(":")
                if int(y[1]) == w:
                    return int(y[0])

        month.template_tasks.clear()
        tasks_ids = []
        dataorderby = month.template_tasks.all()
        for t in tasks:
            tlist = t.split(":")
            torder = int(tlist[0])
            tid = int(tlist[1])
            tasks_ids.append(tid)
            orBy = orderBy.objects.create(
                month=month, templateTask=templateTask(id=tid), ordering=torder
            )

        packages = Package.objects.filter(template=pid).prefetch_related("tasks")
        for package in packages:
            tids = []
            for task in package.tasks.filter(month=month.num):
                getOrd = getOrderding(task.template_task.id)
                if task.template_task.id not in tasks_ids:
                    task.delete()
                elif task.ordering != getOrd:
                    task.ordering = getOrd
                    task.save()
                    tids.append(task.template_task.id)
                else:
                    tids.append(task.template_task.id)

            toSave = []
            for item in tasks_ids:
                if item not in tids:
                    toSave.append(
                        Task(
                            start_date=None,
                            end_date=None,
                            status=None,
                            notes="",
                            report_link="",
                            month=month.num,
                            template_task=templateTask(id=item),
                            ordering=getOrderding(item),
                        )
                    )
            if toSave:
                savedTask = Task.objects.bulk_create(toSave)
                for obj in savedTask:
                    package.tasks.add(obj.id)


class templateTask(models.Model):
    title = models.CharField(max_length=500)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="templateTask"
    )

    def __str__(self):
        return self.title

    def createTask(request):
        templateTask.objects.create(
            title=request.POST["title"], created_by=request.user
        )

    def getAllTask(request):
        task = templateTask.objects.filter(created_by=request.user).all()
        return task

    def getTaskById(request, id):
        task = templateTask.objects.filter(id=id, created_by=request.user).first()
        return task

    def editTask(request, id):
        task = templateTask.objects.filter(id=id).first()
        if not task or task.created_by != request.user:
            return
        task.title = request.POST["title"]
        task.save()

    def removeTask(request, id):
        task = templateTask.objects.filter(id=id).first()
        if not task or task.created_by != request.user:
            return False
        task.delete()
        return True


class addonOrderBy(models.Model):
    templateAddon = models.ForeignKey("templateAddon", on_delete=models.CASCADE)
    templateTask = models.ForeignKey("templateTask", on_delete=models.CASCADE)
    ordering = models.IntegerField()

    def __str__(self):
        return self.templateTask.title


class templateAddon(models.Model):
    title = models.CharField(max_length=500)
    color = models.CharField(max_length=500)
    template_tasks = models.ManyToManyField(
        "templateTask", blank=True, default=None, through="addonOrderBy"
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="templateAddon"
    )

    def __str__(self):
        return self.title

    def getAllAddon(request):
        user = request.user
        addons = user.templateAddon.all()
        return addons

    def createAddon(request):
        templateAddon.objects.create(
            title=request.POST["title"],
            color=request.POST["color"],
            created_by=request.user,
        )

    def editAddon(request, id):
        addon = templateAddon.objects.get(id=id)
        if not addon or addon.created_by != request.user:
            return
        tasks = [x for x in request.POST.getlist("check")]
        tasks_dict = {int(x.split(":")[1]): int(x.split(":")[0]) for x in tasks}
        addon.title = request.POST["title"]
        addon.color = request.POST["color"]
        addon.save()
        addeds = addon.addonorderby_set.all()
        addedsids = []

        for added in addeds:
            addedsids.append(added.templateTask.id)
            if added.templateTask.id in tasks_dict:
                if added.ordering != tasks_dict.get(added.templateTask.id):
                    asets = Addon.objects.filter(template=addon.id)
                    for aset in asets:
                        toreordertasks = aset.tasks.filter(
                            template_task=added.templateTask.id
                        )
                        for x in toreordertasks:
                            x.ordering = tasks_dict.get(added.templateTask.id)
                            x.save()
                    added.ordering = tasks_dict.get(added.templateTask.id)
                    added.save()
            else:
                asets = Addon.objects.filter(template=addon.id)
                for aset in asets:
                    toremovetasks = aset.tasks.filter(
                        template_task=added.templateTask.id
                    )
                    toremovetasks.delete()
                added.delete()

        for dictid in tasks_dict:
            if dictid not in addedsids:
                addTempTask = addonOrderBy.objects.create(
                    templateAddon=addon,
                    templateTask=templateTask(id=dictid),
                    ordering=tasks_dict.get(dictid),
                )
                asets = Addon.objects.filter(template=addon.id)
                for aset in asets:
                    order = aset.order_set.get()
                    newTasks = []
                    for x in range(1, order.month + 1):
                        newTasks.append(
                            Task(
                                start_date=None,
                                status=None,
                                month=x,
                                end_date=None,
                                completed_by=None,
                                notes="",
                                report_link="",
                                template_task=addTempTask.templateTask,
                                ordering=addTempTask.ordering,
                            )
                        )
                    toSave = Task.objects.bulk_create(newTasks)
                    for obj in toSave:
                        aset.tasks.add(obj.id)

    def removeAddon(request, id):
        addon = templateAddon.objects.filter(id=id).first()
        if not addon or addon.created_by != request.user:
            return False
        addon.delete()
        return True

    def getAddonById(id):
        addon = templateAddon.objects.get(id=id)
        return addon


class Addon(models.Model):
    tasks = models.ManyToManyField("Task", blank=True, default=None)
    template = models.ForeignKey(
        "templateAddon", on_delete=models.CASCADE, null=True, blank=True, default=None
    )

    def __str__(self):
        return self.template.title


class Status(models.Model):
    name = models.CharField(max_length=500)
    color = models.CharField(max_length=500)
    val = models.IntegerField()
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="status"
    )

    def __str__(self):
        return self.name

    def getAllStatuses(request):
        user = request.user
        statuses = user.status.all()
        return statuses

    def createStatus(request):
        try:
            status = Status(
                name=request.POST.get("name"),
                color=request.POST.get("color"),
                val=request.POST.get("value"),
                created_by=request.user,
            )
            status.save()
        except BaseException:
            pass

    def getStatusById(request, id):
        return Status.objects.filter(id=id, created_by=request.user).first()

    def editStatus(request, id):
        status = Status.objects.filter(id=id, created_by=request.user).first()
        if status:
            status.name = request.POST.get("name")
            status.color = request.POST.get("color")
            status.val = request.POST.get("value")
            status.save()

    def removeStatus(request, id):
        status = Status.objects.filter(id=id, created_by=request.user).first()
        if status:
            status.delete()


class Form(models.Model):
    title = models.CharField(max_length=500)
    orderinfos = models.JSONField(null=True)
    data = models.JSONField(null=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="form"
    )
    is_service = models.BooleanField(default=False)
    order =  models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="intake_form", default=None, blank=True, null=True
    )

    def __str__(self):
        return self.title

    def createForm(request):
        formname = request.POST["formname"]
        is_service = True if request.POST.get("is_service") else False
        orderinfosset = {"orderinfos": request.POST.getlist("orderinfos")}
        if is_service and 'order' not in orderinfosset['orderinfos']:
            orderinfosset['orderinfos'].insert(0, 'order')
        dataset = {}

        for x in range(0, int(request.POST["totalcount"]) + 1):
            if request.POST.get("textfield" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("textfield" + str(x), False),
                    "type": 0,
                }
            elif request.POST.get("checkboxname" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("checkboxname" + str(x), False),
                    "type": 1,
                    "items": request.POST.getlist("checkboxitem" + str(x)),
                }
            elif request.POST.get("textarea" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("textarea" + str(x), False),
                    "type": 3,
                }

        Form.objects.create(
            title=formname,
            orderinfos=orderinfosset,
            data=dataset,
            created_by=request.user,
            is_service=is_service,
        )

    def editForm(request, id):
        form = Form.objects.filter(id=id, created_by=request.user).first()
        if not form:
            return
        formname = request.POST["formname"]
        orderinfosset = {"orderinfos": request.POST.getlist("orderinfos")}
        dataset = {}

        for x in range(0, int(request.POST["totalcount"]) + 1):
            if request.POST.get("textfield" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("textfield" + str(x), False),
                    "type": 0,
                }
            elif request.POST.get("checkboxname" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("checkboxname" + str(x), False),
                    "type": 1,
                    "items": request.POST.getlist("checkboxitem" + str(x)),
                }
            elif request.POST.get("textarea" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("textarea" + str(x), False),
                    "type": 3,
                }

        form.title = formname
        form.orderinfos = orderinfosset
        form.data = dataset
        form.save()

    def getFormById(request, id):
        return Form.objects.get(id=id, created_by=request.user)

    def getAllForms(request):
        forms = Form.objects.filter(created_by=request.user).all()
        return forms

    def removeForm(request, id):
        form = Form.objects.filter(id=id, created_by=request.user).first()
        if form:
            form.delete()


class ZapierApi(models.Model):
    apikey = models.CharField(max_length=5000)
    created_by = models.ForeignKey(
        CustomUser, null=True, on_delete=models.CASCADE, related_name="key"
    )

    def editKey(request):
        # check if zapier key is empty -> delete it
        zapier_key = request.POST.get("apikey")
        if not zapier_key and request.user.key.first():
            request.user.key.first().delete()
            return
        # validate zapier:
        if "zapier" not in zapier_key:
            messages.error(request, "Your zapier hook url is invalid")
            return
        key = request.user.key.first()
        if not key:
            ZapierApi.objects.create(
                apikey=request.POST.get("apikey"), created_by=request.user
            )
        else:
            key.apikey = request.POST.get("apikey")
            key.save()

    def getKey(request):
        key = request.user.key.first()
        return key


class Agency(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="agency"
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to="agency_logo/", null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_added",)

    def set_default_agency_image(self):
        if self.logo:
            self.logo.delete(save=True)

    def __str__(self):
        return f"Agency {self.id} by {self.owner}"


class Notification(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notification"
    )
    is_read = models.BooleanField(default=False)
    text = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"Notification {self.id} for {self.owner}"


class manageUser:
    def createUser(request):
        if request.POST["email"] and request.POST["password"]:
            if request.POST["password"] == request.POST["repeat-password"]:
                if len(request.POST["password"]) >= 6:
                    client_user = CustomUser.objects.filter(
                        email=request.POST["email"]
                    ).first()
                    if client_user:
                        return False
                    user = CustomUser.objects.create_user(
                        first_name=request.POST["first-name"],
                        last_name=request.POST["last-name"],
                        email=request.POST["email"],
                        password=request.POST["password"],
                        is_staff=True,
                        is_registered=True,
                        is_active=False,
                    )

                    user_agency = Agency(owner=user)
                    user_agency.save()

                    uri = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)

                    mail_subject = "SearchManager.pro - Activate your account"
                    url = (
                        f"{request._current_scheme_host}/signup/activate/{uri}/{token}/"
                    )

                    body = render_to_string(
                        "email/acc_active_email.html",
                        {
                            "user": user,
                            "url": url,
                        },
                    )

                    send_mailjet_email(user, mail_subject, body)

                    # create statuses for the user
                    _create_statuses(user, Status)
                    _create_intake_form(user, Form)
                    return True

    def updateAgency(request):
        if not request.user.is_staff:
            return
        agency = request.user.agency.first()
        if request.FILES.get("agency_logo"):
            agency.logo = request.FILES.get("agency_logo")
        agency.name = request.POST.get("agency_name")
        agency.save()

    def getNotificationById(request, id):
        notification = request.user.notification.get(id=id)
        if notification:
            notification.is_read = True
            notification.save()
            return notification

    def deleteNotification(request, id):
        notification = request.user.notification.get(id=id)
        if notification:
            notification.delete()
            return True
        return False

    def resendConfirmation(request):
        email = request.POST.get("email")
        user = CustomUser.objects.filter(email=email, is_active=False).first()
        if user:
            uri = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            mail_subject = "SearchManager.pro - Activate your account"
            url = f"{request._current_scheme_host}/signup/activate/{uri}/{token}/"

            body = render_to_string(
                "email/acc_active_email.html",
                {
                    "user": user,
                    "url": url,
                },
            )

            send_mailjet_email(user, mail_subject, body)
            return True, "Confirmation link has been sent. Check your email"
        return (
            False,
            "We will send you a confirmation link if this account is registered. Check your email",
        )

    def activateUser(request, uri, token):
        try:
            uid = force_text(urlsafe_base64_decode(uri))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            auth.login(request, user)
            return True
        return False

    def createClientUser(request):
        if request.POST["email"] and request.POST["password"]:
            if request.POST["password"] == request.POST["repeat-password"]:
                if len(request.POST["password"]) >= 6:
                    client_user = CustomUser.objects.filter(
                        email=request.POST["email"]
                    ).first()
                    if client_user:
                        if client_user.is_client and not client_user.is_registered:
                            client_user.first_name = request.POST["first-name"]
                            client_user.last_name = request.POST["last-name"]
                            client_user.set_password(request.POST["password"])
                            client_user.is_registered = True
                            client_user.is_active = True
                            client_user.save()
                            auth.login(request, client_user)
                            return True
                        return False

    def loginUser(request):
        user = auth.authenticate(
            request, email=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return True, ""
        else:
            deactivated_user = UserReplication.objects.filter(
                old_email=request.POST.get("email")
            ).first()
            if deactivated_user:
                user_replica = CustomUser.objects.filter(
                    email=deactivated_user.new_email
                ).first()
                if user_replica.is_deleted and not user_replica.is_active:
                    return (
                        False,
                        "This user is either deleted or deactivated. Please contact your administrator to resolve it",
                    )
            return False, "We couldn't find an account with this credentials"

    def checkIfNeedsConfirmation(request):
        user = CustomUser.objects.filter(email=request.POST["email"]).first()
        if user:
            if user.is_registered and not user.is_active and not user.is_client:
                return True
        return False

    def logoutUser(request):
        auth.logout(request)

    def editPassword(request):
        if len(request.POST.get("password")) >= 6:
            request.user.set_password(request.POST.get("password"))
            request.user.save()

    def editProfile(request):
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.notes = request.POST.get("notes")
        if request.user.is_staff:
            ZapierApi.editKey(request)
        if request.FILES.get("profile_image"):
            request.user.profile_image = request.FILES.get("profile_image")
        request.user.save()

    def getAllUsers():
        users = CustomUser.objects.all().exclude(is_registered=False)
        return users

    def getAllClients(request):
        clients = CustomUser.objects.filter(created_by=request.user).exclude(
            is_deleted=True
        )
        return clients

    def getClientById(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return None
        return client

    def getClientUserByUuid(uuid):
        client = CustomUser.objects.filter(uuid=uuid)
        if not client:
            return None
        return client

    def createClient(request):
        if request.user.is_staff:
            first_client = len(request.user.client.all())
            if CustomUser.objects.filter(email=request.POST.get("email")).first():
                return False, first_client
            email = request.POST.get("email")
            if not email:
                email = (
                    f"{settings.CLIENT_TAG}-{secrets.token_hex(16)}@searchmanager.pro"
                )
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            client = CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                created_by=request.user,
                is_registered=False,
                is_client=True,
                is_active=False,
            )
            client.set_unusable_password()
            client.save()
            return client, first_client

    def checkEmailAvailable(request, email):
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if user.created_by != request.user:
                return False
            if not user.is_registered:
                return True
        return True

    def sendInvitationUrl(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return "You do not have permission to invite this user"

        url = f"{request._current_scheme_host}/signup/invitation/{client.uuid}/"

        body = render_to_string(
            "email/client_invite_email.html",
            {
                "client": client,
                "url": url,
            },
        )

        mail_subject = "SearchManager.pro - client invitation"

        send_mailjet_email(client, mail_subject, body)

        client.confirmation_sent = True
        client.save()

    def editClient(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return

        if not client.is_registered and request.POST.get("email"):
            if client.email != request.POST.get("email"):
                client.email = request.POST.get("email")
        client.first_name = request.POST.get("first_name")
        client.last_name = request.POST.get("last_name")
        client.save()

    def removeClient(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return False
        _delete_user(client)
        return True

    def getUser(id):
        user = CustomUser.objects.filter(id=id).first()
        return user

    def editUser(request, id):
        if "is_active" in request.POST:
            isactive = True
        else:
            isactive = False

        if "is_staff" in request.POST:
            isstaff = True
        else:
            isstaff = False

        if "is_superuser" in request.POST:
            issuperuser = True
        else:
            issuperuser = False
        user = CustomUser.objects.filter(id=id).update(
            email=request.POST["email"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            is_active=isactive,
            is_staff=isstaff,
            is_superuser=issuperuser,
        )

    def editUserPassword(request, id):
        user = CustomUser.objects.get(id=id)
        new_password = request.POST.get("password")
        if len(new_password) >= 6:
            user.set_password(new_password)
            user.save()

    def getNormalUsers(request):
        return request.user.client.all().exclude(is_deleted=True)

    def getStaffUsers():
        users = CustomUser.objects.filter(is_active=True, is_staff=True)
        return users

    def deleteUser(request, id):
        if request.user.is_superuser:
            user = CustomUser.objects.filter(id=id).first()
            for i in user.client.all():
                _delete_user(i)
            _delete_user(user)


class Message(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="message")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.EmailField(max_length=255, null=True, blank=True)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return f"Message {self.id} by {self.author}"
