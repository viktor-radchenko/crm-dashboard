# Generated by Django 3.2.4 on 2022-05-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_crm', '0003_zapierapi_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='recepient',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
