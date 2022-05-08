# Generated by Django 3.2.4 on 2022-05-08 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_crm', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zapierapi',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key', to=settings.AUTH_USER_MODEL),
        ),
    ]
