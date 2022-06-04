# Generated by Django 3.2.4 on 2022-06-04 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_crm', '0008_auto_20220604_0832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='recepient',
            new_name='recipient',
        ),
        migrations.AddField(
            model_name='form',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intake_form', to='app_crm.order'),
        ),
        migrations.AddField(
            model_name='order',
            name='extra_fields',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
