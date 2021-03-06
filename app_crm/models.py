import re

import requests
import json

from django.db import models
from app_users.models import CustomUser
from django.contrib import auth

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
        if order.owner == None:
            if request.user.is_staff:
                return order
            else:
                return False
        else:
            if order.owner.id == request.user.id or request.user.is_staff:
                return order
            else:
                return False

    def createCustomOrder(request):
        order_num = re.sub("\D", "", request.POST["order"])
        userid = CustomUser.objects.get(id=request.POST["userid"])
        stat = Status.objects.filter(val=1).first()
        Order(
            order=order_num,
            company_name=request.POST["company_name"],
            company_address=request.POST["company_address"],
            company_city=request.POST["company_city"],
            company_state=request.POST["company_state"],
            company_zip=request.POST["company_zip"],
            company_country=request.POST["company_country"],
            company_phone=request.POST["company_phone"],
            website_url=request.POST["website_url"],
            company_email=request.POST["company_email"],
            company_description=request.POST["company_description"],
            logo_image=request.POST["logo_image"],
            map_url=request.POST["map_url"],
            website_login_url=request.POST["website_login_url"],
            web_username=request.POST["web_username"],
            web_password=request.POST["web_password"],
            analytics_account=request.POST["analytics_account"],
            start_date=None,
            renewal_date=None,
            status=stat,
            owner=userid,
            month=1,
        ).save()

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
        order.order = re.sub("\D", "", request.POST["order"])
        order.company_name = request.POST["company_name"]
        order.company_address = request.POST["company_address"]
        order.company_city = request.POST["company_city"]
        order.company_state = request.POST["company_state"]
        order.company_zip = request.POST["company_zip"]
        order.company_country = request.POST["company_country"]
        order.company_phone = request.POST["company_phone"]
        order.website_url = request.POST["website_url"]
        order.company_email = request.POST["company_email"]
        order.company_description = request.POST["company_description"]
        order.logo_image = request.POST["logo_image"]
        order.map_url = request.POST["map_url"]
        order.website_login_url = request.POST["website_login_url"]
        order.web_username = request.POST["web_username"]
        order.web_password = request.POST["web_password"]
        order.analytics_account = request.POST["analytics_account"]
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
        order.status = Status.objects.filter(val=0).first()
        order.save()

    def getAllOrders(request):
        user_ids = []
        user_ids.append(request.user.id)
        for client in request.user.client.all():
            user_ids.append(client.id)
        orders = Order.objects.filter(owner__in=user_ids)
        return orders

    def createUserOrder(request):
        order_num = re.sub("\D", "", request.POST["order"])
        owner = CustomUser.objects.get(id=request.user.id)
        stat = Status.objects.filter(val=1).first()
        Order(
            order=order_num,
            company_name=request.POST["company_name"],
            company_address=request.POST["company_address"],
            company_city=request.POST["company_city"],
            company_state=request.POST["company_state"],
            company_zip=request.POST["company_zip"],
            company_country=request.POST["company_country"],
            company_phone=request.POST["company_phone"],
            website_url=request.POST["website_url"],
            company_email=request.POST["company_email"],
            company_description=request.POST["company_description"],
            logo_image=request.POST["logo_image"],
            map_url=request.POST["map_url"],
            website_login_url=request.POST["website_login_url"],
            web_username=request.POST["web_username"],
            web_password=request.POST["web_password"],
            analytics_account=request.POST["analytics_account"],
            start_date=None,
            renewal_date=None,
            status=stat,
            owner=owner,
            month=1,
        ).save()
        return True

    def editUserOrder(request, id):
        order = Order.objects.get(id=id)
        order.order = re.sub("\D", "", request.POST["order"])
        order.company_name = request.POST["company_name"]
        order.company_address = request.POST["company_address"]
        order.company_city = request.POST["company_city"]
        order.company_state = request.POST["company_state"]
        order.company_zip = request.POST["company_zip"]
        order.company_country = request.POST["company_country"]
        order.company_phone = request.POST["company_phone"]
        order.website_url = request.POST["website_url"]
        order.company_email = request.POST["company_email"]
        order.company_description = request.POST["company_description"]
        order.logo_image = request.POST["logo_image"]
        order.map_url = request.POST["map_url"]
        order.website_login_url = request.POST["website_login_url"]
        order.web_username = request.POST["web_username"]
        order.web_password = request.POST["web_password"]
        order.analytics_account = request.POST["analytics_account"]
        order.save()

    def getUserOrders(request):
        orders = Order.objects.filter(owner=request.user.id)
        return orders

    def sendAllInfo(id):
        order = Order.objects.get(id=id)
        if ZapierApi.objects.filter(id=1).exists():
            deliv_link = (
                "https://searchmanager.pro/dashboard/admin/"
                + str(order.id)
                + "/deliverables/"
            )
            apikey = ZapierApi.objects.get(id=1)

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
            }

            r = requests.post(apikey.apikey, data=json.dumps(dataset))
            return r.ok
        else:
            return False

    def sendForm(request, id, formid):
        order = Order.objects.get(id=id)
        if ZapierApi.objects.filter(id=1).exists():
            apikey = ZapierApi.objects.get(id=1)
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

            r = requests.post(apikey.apikey, data=json.dumps(dataset))
            return r.ok
        else:
            return False

    def getOrdersByFilter(request):
        filters = {}
        if request.GET.get("select-package", False):
            filters["package__template_id__in"] = list(
                map(int, request.GET.getlist("select-package"))
            )
        if request.GET.get("select-addon", False):
            filters["addon__template_id__in"] = list(
                map(int, request.GET.getlist("select-addon"))
            )
        if request.GET.get("select-status", False):
            filters["status__in"] = list(map(int, request.GET.getlist("select-status")))
        if request.GET.get("select-user", False):
            filters["owner__in"] = list(map(int, request.GET.getlist("select-user")))
        if request.GET.get("month", False):
            filters["month"] = int(request.GET.get("month"))
        orders = Order.objects.filter(**filters)
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

        if request.POST["completed"] == "None":
            local_completed_by = None
            task.completed_by = local_completed_by
        else:
            local_completed_by = CustomUser.objects.get(
                id=int(request.POST["completed"])
            )
            task.completed_by = local_completed_by

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
                completed_by=local_completed_by,
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
    val = models.IntegerField(default=None, null=True, unique=True)
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
        status = Status.objects.filter(id=id, created_by=request.user)
        if status:
            status.update(
                name=request.POST.get("name"),
                color=request.POST.get("color"),
                val=request.POST.get("value"),
            )

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

    def __str__(self):
        return self.title

    def createForm(request):
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
            elif request.POST.get("radioname" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("radioname" + str(x), False),
                    "type": 2,
                    "items": request.POST.getlist("radioitem" + str(x)),
                }

        Form.objects.create(
            title=formname,
            orderinfos=orderinfosset,
            data=dataset,
            created_by=request.user,
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
            elif request.POST.get("radioname" + str(x), False):
                dataset[x] = {
                    "title": request.POST.get("radioname" + str(x), False),
                    "type": 2,
                    "items": request.POST.getlist("radioitem" + str(x)),
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

    def editKey(request):
        if ZapierApi.objects.filter(id=1).exists():
            ZapierApi.objects.filter(id=1).update(apikey=request.POST.get("apikey"))
        else:
            ZapierApi.objects.create(id=1, apikey=request.POST.get("apikey"))

    def getKey():
        key = ZapierApi.objects.filter(id=1)
        return key


class manageUser:
    def createUser(request):
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
                            client_user.save()
                            auth.login(request, client_user)
                            return True
                        return False
                    else:
                        user = CustomUser.objects.create_user(
                            first_name=request.POST["first-name"],
                            last_name=request.POST["last-name"],
                            email=request.POST["email"],
                            password=request.POST["password"],
                            is_staff=True,
                        )
                        auth.login(request, user)
                        return True

    def loginUser(request):
        user = auth.authenticate(
            request, email=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return True
        else:
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
        request.user.save()

    def getAllUsers():
        users = CustomUser.objects.all()
        return users

    def getAllClients(request):
        clients = CustomUser.objects.filter(created_by=request.user, is_active=True)
        return clients

    def getClientById(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return None
        return client

    def createClient(request):
        if request.user.is_staff:
            if CustomUser.objects.filter(email=request.POST.get("email")).first():
                return False
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            client = CustomUser.objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                created_by=request.user,
                is_registered=False,
                is_client=True,
            )
            client.set_unusable_password()
            client.save()
            return client

    def editClient(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        client.first_name = first_name
        client.last_name = last_name
        client.save()

    def removeClient(request, id):
        client = CustomUser.objects.get(id=id)
        if not client or client.created_by != request.user:
            return False
        client.is_active = False

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
        return request.user.client.all()

    def getStaffUsers():
        users = CustomUser.objects.filter(is_active=True, is_staff=True)
        return users

    def deleteUser(request, id):
        if request.user.is_superuser:
            CustomUser.objects.filter(id=id).delete()


class Message(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="message")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return f"Message {self.id} by {self.author}"
