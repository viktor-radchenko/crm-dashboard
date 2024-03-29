# Generated by Django 3.2.4 on 2022-08-18 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='addonOrderBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('color', models.CharField(max_length=500)),
                ('val', models.IntegerField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, default=None, null=True)),
                ('end_date', models.DateField(blank=True, default=None, null=True)),
                ('notes', models.TextField(blank=True, default=None)),
                ('month', models.IntegerField(blank=True, default=None)),
                ('ordering', models.IntegerField()),
                ('completed_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='completed_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app_crm.status')),
            ],
        ),
        migrations.CreateModel(
            name='ZapierApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apikey', models.CharField(max_length=5000)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='templateTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templateTask', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='templatePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('color', models.CharField(max_length=500)),
                ('num_of_month', models.IntegerField(blank=True, default=None)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='temlpatePackage', to=settings.AUTH_USER_MODEL)),
                ('month', models.ManyToManyField(blank=True, default=None, to='app_crm.Month')),
            ],
        ),
        migrations.CreateModel(
            name='templateAddon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('color', models.CharField(max_length=500)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='templateAddon', to=settings.AUTH_USER_MODEL)),
                ('template_tasks', models.ManyToManyField(blank=True, default=None, through='app_crm.addonOrderBy', to='app_crm.templateTask')),
            ],
        ),
        migrations.CreateModel(
            name='TaskReportLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=2048)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_link', to='app_crm.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='template_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.templatetask'),
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasks', models.ManyToManyField(blank=True, default=None, to='app_crm.Task')),
                ('template', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_crm.templatepackage')),
            ],
        ),
        migrations.CreateModel(
            name='orderBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.IntegerField()),
                ('month', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.month')),
                ('templateTask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.templatetask')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.CharField(max_length=500)),
                ('company_name', models.CharField(max_length=5000)),
                ('company_address', models.CharField(max_length=5000)),
                ('company_city', models.CharField(max_length=5000)),
                ('company_state', models.CharField(max_length=5000)),
                ('company_zip', models.CharField(max_length=5000)),
                ('company_country', models.CharField(max_length=5000)),
                ('company_phone', models.CharField(max_length=5000)),
                ('website_url', models.CharField(max_length=5000)),
                ('company_email', models.CharField(max_length=5000)),
                ('company_description', models.CharField(max_length=5000)),
                ('logo_image', models.CharField(max_length=5000)),
                ('map_url', models.CharField(max_length=5000)),
                ('website_login_url', models.CharField(max_length=5000)),
                ('web_username', models.CharField(max_length=5000)),
                ('web_password', models.CharField(max_length=5000)),
                ('analytics_account', models.CharField(max_length=5000)),
                ('link1', models.CharField(max_length=10000)),
                ('link2', models.CharField(max_length=10000)),
                ('link3', models.CharField(max_length=10000)),
                ('link4', models.CharField(max_length=10000)),
                ('start_date', models.DateField(blank=True, default=None, null=True)),
                ('renewal_date', models.DateField(blank=True, default=None, null=True)),
                ('extra_fields', models.JSONField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('month', models.IntegerField(blank=True, default=None)),
                ('is_deleted', models.BooleanField(default=False)),
                ('addon', models.ManyToManyField(blank=True, default=None, to='app_crm.Addon')),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='order', to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app_crm.package')),
                ('status', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='app_crm.status')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='month',
            name='template_tasks',
            field=models.ManyToManyField(blank=True, default=None, through='app_crm.orderBy', to='app_crm.templateTask'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.EmailField(blank=True, max_length=255, null=True)),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='app_crm.order')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app_crm.message')),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('orderinfos', models.JSONField(null=True)),
                ('data', models.JSONField(null=True)),
                ('zapier_tag', models.TextField(blank=True, null=True)),
                ('is_service', models.BooleanField(default=False)),
                ('is_snapshot', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intake_form', to='app_crm.order')),
            ],
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='agency_logo/')),
                ('notes', models.TextField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agency', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date_added',),
            },
        ),
        migrations.AddField(
            model_name='addonorderby',
            name='templateAddon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.templateaddon'),
        ),
        migrations.AddField(
            model_name='addonorderby',
            name='templateTask',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_crm.templatetask'),
        ),
        migrations.AddField(
            model_name='addon',
            name='tasks',
            field=models.ManyToManyField(blank=True, default=None, to='app_crm.Task'),
        ),
        migrations.AddField(
            model_name='addon',
            name='template',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_crm.templateaddon'),
        ),
    ]
