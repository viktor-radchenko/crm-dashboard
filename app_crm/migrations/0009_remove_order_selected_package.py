# Generated by Django 3.2.4 on 2022-08-08 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_crm', '0008_order_selected_package'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='selected_package',
        ),
    ]
