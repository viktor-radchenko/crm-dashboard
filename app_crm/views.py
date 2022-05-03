import re
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model

from app_crm.models import (
    Order,
    Package,
    Task,
    templatePackage,
    Month,
    templateTask,
    manageUser,
    Status,
    templateAddon,
    Addon,
    Form,
    ZapierApi,
    Message,
)


class sign:
    def signin(request):
        if request.user.is_authenticated:
            return redirect("/dashboard/admin/allorders/")
        else:
            if request.method == "POST":
                if manageUser.checkIfNeedsConfirmation(request):
                    messages.warning(request, "You need to confirm your account first. Please check your email")
                    return redirect("/")
                if manageUser.loginUser(request):
                    return redirect("/dashboard/admin/allorders/")
                else:
                    context = {}
                    context["error_message"] = "Wrong email or password"
                    return render(request, "signin.html", context)
            return render(request, "signin.html")

    def signup(request):
        if request.user.is_authenticated:
            return redirect("/dashboard/admin/allorders/")
        else:
            if request.method == "POST":
                if manageUser.createUser(request):
                    return render(request, "confirm_email.html")
                else:
                    context = {}
                    context["error_message"] = "This account already exists"
                    return render(request, "signup.html", context)
            return render(request, "signup.html")

    def invitationSignUp(request, uuid):
        if request.user.is_authenticated:
            return redirect("/dashboard/admin/allorders/")
        user = get_user_model().objects.filter(uuid=uuid).first()
        if not user:
            messages.error(request, "No client found with this id. Contact administrator and request new confirmation link")
            return redirect("/")
        if request.method == "POST":
            if manageUser.createClientUser(request):
               return redirect("/dashboard/profile/")
            else:
                context = {}
                context["error_message"] = "This account already exists"
                return render(request, "signup.html", context)

        context = dict(
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name
        )

        return render(request, "signup.html", context)

    def activateAccount(request, uri, token):
        if manageUser.activateUser(request, uri, token):
            messages.success(request, "You have successfully activated you account")
            return redirect('/')
        return HttpResponse('Activation link is invalid!')

    def logout(request):
        manageUser.logoutUser(request)
        return redirect("/")


class dash:
    def dashboardProfile(request):
        if request.user.is_authenticated:
            if "editProfile" in request.POST:
                manageUser.editProfile(request)
            elif "editPassword" in request.POST:
                manageUser.editPassword(request)
            return render(request, "dashboard/profile.html")
        else:
            return redirect("/")

    class admin:
        def allOrders(request):
            if request.user.is_staff:
                context = {}
                context["packages"] = templatePackage.getAllPackage(request)
                context["addons"] = templateAddon.getAllAddon(request)
                context["statuses"] = Status.getAllStatuses(request)
                context["users"] = manageUser.getNormalUsers(request)
                if request.GET:
                    context["orders"] = Order.getOrdersByFilter(request)
                else:
                    context["orders"] = Order.getAllOrders(request)
                return render(request, "dashboard/admin/allorders.html", context)
            else:
                return redirect("/dashboard/user/myorders/")

        def createCustomOrder(request):
            if request.user.is_staff:
                clients = request.user.client.all()
                if not clients:
                    messages.warning(request, 'You need to add a client first')
                    return redirect("/dashboard/admin/clients/create/")
                if request.method == "POST":
                    Order.createCustomOrder(request)
                    return redirect("/dashboard/admin/allorders")
                context = {}
                context["users"] = manageUser.getAllClients(request)
                context['client_tag'] = settings.CLIENT_TAG
                return render(request, "dashboard/admin/createcustom.html", context)
            else:
                return redirect("/")

        def deleteOrder(request, id):
            if request.user.is_superuser:
                Order.deleteOrder(id)
                return redirect("/dashboard/admin/allorders/")
            else:
                return redirect("/")

        def editInfo(request, id):
            if request.user.is_staff:
                if request.method == "POST":
                    Order.editInfo(request, id)
                    return redirect("/dashboard/admin/allorders")
                context = {}
                context["order"] = Order.getOrderById(request, id)
                return render(request, "dashboard/admin/editinfo.html", context)
            else:
                return redirect("/")

        def editOrder(request, id):
            if request.user.is_staff:
                if request.method == "POST":
                    Order.editOrder(request, id)
                    return redirect("/dashboard/admin/allorders")
                context = {}
                order = Order.getOrderById(request, id)
                context["order"] = order
                addons = order.addon.all()
                context["addons"] = addons
                context["template_addons_ids"] = [x.template.id for x in addons]
                context["statuses"] = Status.getAllStatuses(request)
                context["package"] = templatePackage.getAllPackage(request)
                context["template_addons"] = templateAddon.getAllAddon(request)
                context["users"] = manageUser.getAllClients(request)
                return render(request, "dashboard/admin/edit.html", context)
            else:
                return redirect("/")

        def cancelOrder(request, id):
            if request.user.is_staff:
                Order.cancelOrder(id)
                return redirect("/dashboard/admin/allorders")
            else:
                return redirect("/")

        def deliverables(request, id):
            if request.user.is_staff:
                order = Order.getOrderById(request, id)
                context = {}
                if order.package != None:
                    context["package"] = order.package
                    context["task"] = order.package.tasks.all()
                context["order"] = order
                context["statuses"] = Status.getAllStatuses(request)
                context["addons"] = order.addon.all()
                context["users"] = manageUser.getStaffUsers()
                context["month"] = list(range(1, order.month + 1))
                context["forms"] = Form.getAllForms(request)
                return render(request, "dashboard/admin/deliverables.html", context)
            else:
                return redirect("/")

        def task(request, oid, id):
            if request.user.is_staff:
                if request.method == "POST":
                    Task.editTask(request, id)
                    return redirect("/dashboard/admin/" + str(oid) + "/deliverables/")
                return redirect("/dashboard/admin/" + str(oid) + "/deliverables/")
            else:
                return redirect("/")

        def allClients(request):
            if request.user.is_staff:
                context = {}
                context["clients"] = manageUser.getAllClients(request)
                return render(request, "dashboard/admin/clients/clients.html", context)
            else:
                return redirect("/")

        def clientsCreate(request):
            if request.user.is_staff:
                if request.method == "POST":
                    if request.POST.get("email") or (request.POST.get("first_name") or request.POST.get("last_name")):
                        client = manageUser.createClient(request)
                        if client:
                            return redirect("/dashboard/admin/clients/")
                        messages.error(request, "Client with this email is already created")
                    else:
                        messages.error(request, "Form cannot be empty. Please fill in one of the fileds below")
                return render(request, "dashboard/admin/clients/create.html")
            else:
                return redirect("/")

        def clientsEdit(request, id):
            if request.user.is_staff:
                if request.method == "POST":
                    email = request.POST.get("email")
                    if email:
                        if manageUser.checkExistingClientByEmail(email):
                            messages.error(request, "This email is already taken. Try another email")
                            return redirect(f"/dashboard/admin/clients/edit/{id}/")
                    manageUser.editClient(request, id)
                    return redirect(f"/dashboard/admin/clients/edit/{id}/")
                context = {}
                client = manageUser.getClientById(request, id)
                if not client:
                    return redirect("/")
                context["email"] = client.email if settings.CLIENT_TAG not in client.email else '' 
                context["first_name"] = client.first_name
                context["last_name"] = client.last_name
                context["id"] = client.id
                context["registered"] = client.is_registered
                context["disabled"] = 'disabled' if client.is_active and client.is_registered else ''
                return render(request, "dashboard/admin/clients/edit.html", context)
            else:
                return redirect("/")

        def clientsSendInvitation(request, id):
            error = manageUser.sendInvitationUrl(request, id)
            if error:
                messages.error(request, error)
            else:    
                messages.success(request, "Invitation has been sent")
            return redirect(f"/dashboard/admin/clients/edit/{id}/")

        def clientsRemove(request, id):
            if request.user.is_staff:
                if manageUser.removeClient(request, id):
                    return redirect("/dashboard/admin/clients/")
            else:
                return redirect("/")

        def allUsers(request):
            if request.user.is_superuser:
                context = {}
                context["users"] = manageUser.getAllUsers()
                return render(request, "dashboard/admin/users/allusers.html", context)
            else:
                return redirect("/")

        def allUsersEdit(request, id):
            if request.user.is_superuser:
                if request.method == "POST":
                    if "editUser" in request.POST:
                        manageUser.editUser(request, id)
                    elif "editUserPassword" in request.POST:
                        manageUser.editUserPassword(request, id)
                    return redirect("/dashboard/admin/allusers")
                context = {}
                context["user"] = manageUser.getUser(id)
                return render(request, "dashboard/admin/users/edit.html", context)
            else:
                return redirect("/")

        def allUsersDelete(request, id):
            if request.user.is_superuser:
                manageUser.deleteUser(request, id)
                return redirect("/dashboard/admin/allusers/")
            else:
                return redirect("/")

        def statuses(request):
            if request.user.is_staff:
                context = {}
                context["statuses"] = Status.getAllStatuses(request)
                return render(
                    request, "dashboard/admin/statuses/statuses.html", context
                )
            else:
                return redirect("/")

        def statusesCreate(request):
            if request.user.is_staff:
                if request.method == "POST":
                    Status.createStatus(request)
                    return redirect("/dashboard/admin/statuses/")
                return render(request, "dashboard/admin/statuses/create.html")
            else:
                return redirect("/")

        def statusesEdit(request, id):
            if request.user.is_staff:
                if request.method == "POST":
                    Status.editStatus(request, id)
                    return redirect("/dashboard/admin/statuses/")
                context = {}
                context["status"] = Status.getStatusById(request, id)
                return render(request, "dashboard/admin/statuses/edit.html", context)
            else:
                return redirect("/")

        def statusesRemove(request, id):
            if request.user.is_staff:
                Status.removeStatus(request, id)
                return redirect("/dashboard/admin/statuses/")
            else:
                return redirect("/")

        def forms(request):
            if request.user.is_staff:
                context = {}
                context["forms"] = Form.getAllForms(request)
                return render(request, "dashboard/admin/forms/forms.html", context)
            else:
                return redirect("/")

        def formsCreate(request):
            if request.user.is_staff:
                if request.method == "POST":
                    Form.createForm(request)
                    return redirect("/dashboard/admin/forms/")
                return render(request, "dashboard/admin/forms/create.html")
            else:
                return redirect("/")

        def formsEdit(request, id):
            if request.user.is_staff:
                if request.method == "POST":
                    Form.editForm(request, id)
                    return redirect("/dashboard/admin/forms/")
                context = {}
                thisform = Form.getFormById(request, id)
                context["form"] = thisform
                context["things"] = thisform.data.values()
                return render(request, "dashboard/admin/forms/edit.html", context)
            else:
                return redirect("/")

        def formsRemove(request, id):
            if request.user.is_staff:
                Form.removeForm(id)
                return redirect("/dashboard/admin/forms/")
            else:
                return redirect("/")

        def keyEdit(request):
            if request.user.is_superuser:
                if request.method == "POST":
                    ZapierApi.editKey(request)
                    return redirect("/dashboard/profile/")
                context = {}
                context["key"] = ZapierApi.getKey()
                return render(request, "dashboard/admin/editkey.html", context)
            else:
                return redirect("/")

        class template:
            def allPackage(request):
                if request.user.is_staff:
                    context = {}
                    context["package"] = templatePackage.getAllPackage(request)
                    return render(
                        request, "dashboard/admin/template/package.html", context
                    )
                else:
                    return redirect("/")

            def createPackage(request):
                if request.user.is_staff:
                    if request.method == "POST":
                        result = templatePackage.createPackage(request)
                        return redirect(
                            "/dashboard/admin/template/package/edit/"
                            + str(result)
                            + "/"
                        )
                    return render(
                        request, "dashboard/admin/template/create_package.html"
                    )
                else:
                    return redirect("/")

            def editPackage(request, id):
                if request.user.is_staff:
                    if request.method == "POST":
                        templatePackage.editPackage(request, id)
                        return redirect(
                            "/dashboard/admin/template/package/edit/" + str(id) + "/"
                        )
                    context = {}
                    pack = templatePackage.getPackageById(id)
                    if pack == None:
                        raise Http404
                    else:
                        context["package"] = pack
                        context["months"] = pack.month.all()
                        return render(
                            request,
                            "dashboard/admin/template/edit_package.html",
                            context,
                        )
                else:
                    return redirect("/")

            def removePackage(request, id):
                if request.user.is_staff:
                    templatePackage.removePackage(request, id)
                    return redirect("/dashboard/admin/template/package")
                else:
                    return redirect("/")

            def editMonth(request, pid, id):
                if request.user.is_staff:
                    if request.method == "POST":
                        Month.editMonth(request, pid, id)
                        return redirect(
                            "/dashboard/admin/template/package/edit/" + str(pid) + "/"
                        )
                    context = {}
                    month = Month.getMonthById(id)
                    context["month"] = month
                    context["ids"] = [x.id for x in month.template_tasks.all()]
                    context["checkedtasks"] = month.orderby_set.all()
                    context["tasks"] = templateTask.getAllTask(request)
                    return render(
                        request, "dashboard/admin/template/edit_month.html", context
                    )
                else:
                    return redirect("/")

            def allTask(request):
                if request.user.is_staff:
                    context = {}
                    context["task"] = templateTask.getAllTask(request)
                    return render(
                        request, "dashboard/admin/template/task.html", context
                    )
                else:
                    return redirect("/")

            def createTask(request):
                if request.user.is_staff:
                    if request.method == "POST":
                        templateTask.createTask(request)
                        return redirect("/dashboard/admin/template/task")
                    return render(request, "dashboard/admin/template/create_task.html")
                else:
                    return redirect("/")

            def editTask(request, id):
                if request.user.is_staff:
                    if request.method == "POST":
                        templateTask.editTask(request, id)
                        return redirect("/dashboard/admin/template/task")
                    context = {}
                    ta = templateTask.getTaskById(request, id)
                    if ta == None:
                        raise Http404
                    else:
                        context["task"] = ta
                        return render(
                            request, "dashboard/admin/template/edit_task.html", context
                        )
                else:
                    return redirect("/")

            def removeTask(request, id):
                if request.user.is_staff:
                    if templateTask.removeTask(request, id):
                        return redirect("/dashboard/admin/template/task")
                else:
                    return redirect("/")

            def allAddon(request):
                if request.user.is_staff:
                    context = {}
                    context["addons"] = templateAddon.getAllAddon(request)
                    return render(
                        request, "dashboard/admin/template/addon.html", context
                    )
                else:
                    return redirect("/")

            def createAddon(request):
                if request.user.is_staff:
                    if request.method == "POST":
                        templateAddon.createAddon(request)
                        return redirect("/dashboard/admin/template/addon")
                    return render(request, "dashboard/admin/template/create_addon.html")
                else:
                    return redirect("/")

            def editAddon(request, id):
                if request.user.is_staff:
                    if request.method == "POST":
                        templateAddon.editAddon(request, id)
                        return redirect("/dashboard/admin/template/addon")
                    context = {}
                    addon = templateAddon.getAddonById(id)
                    context["addon"] = addon
                    context["ids"] = [x.id for x in addon.template_tasks.all()]
                    context["checkedtasks"] = addon.addonorderby_set.all()
                    context["tasks"] = templateTask.getAllTask(request)
                    return render(
                        request, "dashboard/admin/template/edit_addon.html", context
                    )
                else:
                    return redirect("/")

            def removeAddon(request, id):
                if request.user.is_staff:
                    if templateAddon.removeAddon(request, id):
                        return redirect("/dashboard/admin/template/addon")
                else:
                    return redirect("/")

        class send:
            def sendAllInfo(request, id):
                if request.user.is_staff:
                    send = Order.sendAllInfo(id)
                    if send:
                        return redirect("/dashboard/admin/allorders/")
                    else:
                        return handler500(request)
                else:
                    return redirect("/")

            def sendForm(request, id, formid):
                if request.user.is_staff:
                    if request.method == "POST":
                        send = Order.sendForm(request, id, formid)
                        if send:
                            return redirect(
                                "/dashboard/admin/" + str(id) + "/deliverables/"
                            )
                        else:
                            return handler500(request)
                    else:
                        return handler404(request)
                else:
                    return redirect("/")

    class user:
        def myOrders(request):
            if (
                request.user.is_active
                and not request.user.is_staff
                and not request.user.is_superuser
            ):
                context = {}
                context["orders"] = Order.getUserOrders(request)
                return render(request, "dashboard/user/myorders.html", context)
            else:
                return redirect("/")

        def createOrder(request):
            if (
                request.user.is_active
                and not request.user.is_staff
                and not request.user.is_superuser
            ):
                if request.method == "POST":
                    if Order.createUserOrder(request):
                        return redirect("/dashboard/user/myorders")
                return render(request, "dashboard/user/create.html")
            else:
                return redirect("/")

        def editOrder(request, id):
            if (
                request.user.is_active
                and not request.user.is_staff
                and not request.user.is_superuser
            ):
                order = Order.getOrderById(request, id)
                if order != False:
                    if request.method == "POST":
                        Order.editUserOrder(request, id)
                        return redirect("/dashboard/user/myorders")
                    context = {}
                    context["order"] = order
                    return render(request, "dashboard/user/edit.html", context)
                raise Http404
            else:
                return redirect("/")

    class OrderChat:
        def getAllMessages(request, id):
            order = Order.getOrderById(request, id)
            if order and (
                order.owner == request.user or order.owner.created_by == request.user
            ):
                if request.method == "POST":
                    body = request.POST.get("message-body", "")
                    msg = Message(order=order, author=request.user, body=body)

                    # check if message is reply
                    is_reply = int(request.POST.get("replyto", 0))
                    if is_reply:
                        parent = Message.objects.get(id=is_reply)
                        msg.parent = parent

                    msg.save()
                    # send notification to zap

                    return redirect(f"/dashboard/chatroom/{order.id}/")
                context = {}
                context["order"] = order
                context["chat_messages"] = order.message.filter(parent__isnull=True)
                return render(request, "dashboard/admin/chat/messages.html", context)
            return redirect("/")

        def editMessage(request, id):
            message = Message.objects.get(id=id)
            if not message or message.author != request.user:
                return redirect("/")
            if request.method == "POST":
                body = request.POST.get("message-body", "")
                message.body = body
                message.save()
                return redirect(f"/dashboard/chatroom/{message.order.id}/")
            context = dict(message=message)
            return render(request, "dashboard/admin/chat/edit.html", context)


def handler404(request, *args, **argv):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, "500.html")
    response.status_code = 500
    return response
