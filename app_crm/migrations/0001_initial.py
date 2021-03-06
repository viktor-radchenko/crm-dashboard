# Generated by Django 3.2.4 on 2022-04-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Addon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="addonOrderBy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordering", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Form",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("orderinfos", models.JSONField(null=True)),
                ("data", models.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("-date_added",),
            },
        ),
        migrations.CreateModel(
            name="Month",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("num", models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.CharField(max_length=500)),
                ("company_name", models.CharField(max_length=5000)),
                ("company_address", models.CharField(max_length=5000)),
                ("company_city", models.CharField(max_length=5000)),
                ("company_state", models.CharField(max_length=5000)),
                ("company_zip", models.CharField(max_length=5000)),
                ("company_country", models.CharField(max_length=5000)),
                ("company_phone", models.CharField(max_length=5000)),
                ("website_url", models.CharField(max_length=5000)),
                ("company_email", models.CharField(max_length=5000)),
                ("company_description", models.CharField(max_length=5000)),
                ("logo_image", models.CharField(max_length=5000)),
                ("map_url", models.CharField(max_length=5000)),
                ("website_login_url", models.CharField(max_length=5000)),
                ("web_username", models.CharField(max_length=5000)),
                ("web_password", models.CharField(max_length=5000)),
                ("analytics_account", models.CharField(max_length=5000)),
                ("link1", models.CharField(max_length=10000)),
                ("link2", models.CharField(max_length=10000)),
                ("link3", models.CharField(max_length=10000)),
                ("link4", models.CharField(max_length=10000)),
                ("note", models.TextField()),
                ("start_date", models.DateField(blank=True, default=None, null=True)),
                ("renewal_date", models.DateField(blank=True, default=None, null=True)),
                ("month", models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name="orderBy",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ordering", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Package",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=500)),
                ("color", models.CharField(max_length=500)),
                ("val", models.IntegerField(default=None, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_date", models.DateField(blank=True, default=None, null=True)),
                ("end_date", models.DateField(blank=True, default=None, null=True)),
                ("notes", models.TextField(blank=True, default=None)),
                ("report_link", models.CharField(blank=True, max_length=10000)),
                ("month", models.IntegerField(blank=True, default=None)),
                ("ordering", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="templateAddon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("color", models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="templatePackage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("color", models.CharField(max_length=500)),
                ("num_of_month", models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name="templateTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name="ZapierApi",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("apikey", models.CharField(max_length=5000)),
            ],
        ),
    ]
