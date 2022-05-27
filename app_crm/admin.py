from django.contrib import admin
from app_crm.models import (
    Task,
    Package,
    Order,
    templateTask,
    templatePackage,
    Month,
    orderBy,
    Addon,
    templateAddon,
    addonOrderBy,
    Status,
    Form,
    ZapierApi,
    Agency,
)

# Register your models here.


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ("order", "owner")
    search_fields = ("order",)


@admin.register(templateTask)
class templateTask(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(templatePackage)
class templatePackage(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Task)
class Task(admin.ModelAdmin):
    list_display = ("template_task",)
    search_fields = ("template_task",)


@admin.register(Package)
class Package(admin.ModelAdmin):
    list_display = ("template",)
    search_fields = ("template",)


@admin.register(Month)
class Month(admin.ModelAdmin):
    list_display = ("num",)
    search_fields = ("num",)


@admin.register(orderBy)
class orderBy(admin.ModelAdmin):
    list_display = ("ordering",)


@admin.register(Addon)
class Addon(admin.ModelAdmin):
    list_display = ("template",)


@admin.register(templateAddon)
class templateAddon(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(addonOrderBy)
class addonOrderBy(admin.ModelAdmin):
    list_display = ("ordering",)


@admin.register(Status)
class Status(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Form)
class Form(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(ZapierApi)
class ZapierApi(admin.ModelAdmin):
    list_display = ("apikey",)


@admin.register(Agency)
class Agency(admin.ModelAdmin):
    list_display = ("owner",)
