from app_crm import views
from django.urls import path, include


app_name = "app_crm"

urlpatterns = [
    path("", views.sign.signin),
    path("signup/", include(
        [
            path("", views.sign.signup),
            path("confirmation/resend/", views.sign.resendConfirmation),
            path("invitation/<str:uuid>/", views.sign.invitationSignUp),
            path("activate/<uri>/<token>/", views.sign.activateAccount),
        ]
    )),
    path("logout/", views.sign.logout),
    path("notifications/", include(
        [
            path("", views.dash.getAllNotifications),
            path("<id>/", views.dash.getNotificationById),
            path("delete/<int:id>/", views.dash.deleteNotification),
            
        ]
    )),
    path(
        "dashboard/",
        include(
            [
                path("profile/", include(
                    [
                        path("", views.dash.dashboardProfile),
                        path("deleteImg/", views.dash.deleteImage),
                        path("deleteAgencyLogo/", views.dash.deleteAgencyLogo),
                    ]
                )),
                path(
                    "admin/",
                    include(
                        [
                            path(
                                "allorders/",
                                views.dash.admin.allOrders,
                                name="allOrders",
                            ),
                            path("cleanfilters/", views.dash.admin.cleanFilters),
                            path("create/", views.dash.admin.createCustomOrder),
                            path("delete/<int:id>/", views.dash.admin.deleteOrder),
                            path("edit/<int:id>/", views.dash.admin.editOrder),
                            path("editinfo/<int:id>/", views.dash.admin.editInfo),
                            path("cancel/<int:id>/", views.dash.admin.cancelOrder),
                            path(
                                "<int:id>/deliverables/",
                                views.dash.admin.deliverables,
                                name="deliverables",
                            ),
                            path(
                                "<int:oid>/deliverables/task/<int:id>/",
                                views.dash.admin.task,
                            ),
                            path(
                                "<int:id>/deliverables/form/all/",
                                views.dash.admin.send.sendAllInfo,
                            ),
                            path(
                                "<int:id>/deliverables/form/<int:formid>/",
                                views.dash.admin.send.sendForm,
                            ),
                            path(
                                "template/",
                                include(
                                    [
                                        path(
                                            "package/",
                                            views.dash.admin.template.allPackage,
                                        ),
                                        path(
                                            "package/create/",
                                            views.dash.admin.template.createPackage,
                                        ),
                                        path(
                                            "package/edit/<int:id>/",
                                            views.dash.admin.template.editPackage,
                                        ),
                                        path(
                                            "package/edit/<int:pid>/month/<int:id>/",
                                            views.dash.admin.template.editMonth,
                                        ),
                                        path(
                                            "package/remove/<int:id>/",
                                            views.dash.admin.template.removePackage,
                                        ),
                                        path(
                                            "task/", views.dash.admin.template.allTask
                                        ),
                                        path(
                                            "task/create/",
                                            views.dash.admin.template.createTask,
                                        ),
                                        path(
                                            "task/edit/<int:id>/",
                                            views.dash.admin.template.editTask,
                                        ),
                                        path(
                                            "task/remove/<int:id>/",
                                            views.dash.admin.template.removeTask,
                                        ),
                                        path(
                                            "addon/", views.dash.admin.template.allAddon
                                        ),
                                        path(
                                            "addon/create/",
                                            views.dash.admin.template.createAddon,
                                        ),
                                        path(
                                            "addon/edit/<int:id>/",
                                            views.dash.admin.template.editAddon,
                                        ),
                                        path(
                                            "addon/remove/<int:id>/",
                                            views.dash.admin.template.removeAddon,
                                        ),
                                    ]
                                ),
                            ),
                            path("statuses/", views.dash.admin.statuses),
                            path("statuses/create/", views.dash.admin.statusesCreate),
                            path(
                                "statuses/edit/<int:id>/", views.dash.admin.statusesEdit
                            ),
                            path(
                                "statuses/remove/<int:id>/",
                                views.dash.admin.statusesRemove,
                            ),
                            path("forms/", views.dash.admin.forms),
                            path("forms/create/", views.dash.admin.formsCreate),
                            path("forms/edit/<int:id>/", views.dash.admin.formsEdit),
                            path(
                                "forms/remove/<int:id>/", views.dash.admin.formsRemove
                            ),
                            path("services/", views.dash.admin.serviceForms),
                            path("services/create/", views.dash.admin.serviceFormsCreate),
                            path("services/edit/<int:id>/", views.dash.admin.serviceFormsEdit),
                            path(
                                "services/remove/<int:id>/", views.dash.admin.formsRemove
                            ),
                            path("clients/", views.dash.admin.allClients),
                            path("clients/create/", views.dash.admin.clientsCreate),
                            path(
                                "clients/edit/<int:id>/", views.dash.admin.clientsEdit
                            ),
                            path(
                                "clients/sendinvitation/<int:id>/", views.dash.admin.clientsSendInvitation
                            ),
                            path(
                                "clients/remove/<int:id>/",
                                views.dash.admin.clientsRemove,
                            ),
                            path("allusers/", views.dash.admin.allUsers),
                            path("allusers/<int:id>/", views.dash.admin.allUsersEdit),
                            path(
                                "allusers/<int:id>/delete/",
                                views.dash.admin.allUsersDelete,
                            ),
                            path("editkey/", views.dash.admin.keyEdit),
                        ]
                    ),
                ),
                path(
                    "user/",
                    include(
                        [
                            path("myorders/", views.dash.user.myOrders),
                            path("create/", views.dash.user.createOrder),
                            path("edit/<int:id>/", views.dash.user.editOrder),
                        ]
                    ),
                ),
                path("chatroom/<int:id>/", views.dash.OrderChat.getAllMessages),
                path("chatroom/edit/<int:id>/", views.dash.OrderChat.editMessage),
            ]
        ),
    ),
]

handler404 = "app_crm.views.handler404"
handler500 = "app_crm.views.handler500"
