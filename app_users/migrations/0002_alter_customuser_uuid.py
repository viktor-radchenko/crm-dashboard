# Generated by Django 3.2.4 on 2022-05-08 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='uuid',
            field=models.CharField(default='748d87f2410c27290f8152b139ddfd94474565d44f5c225f869662fa89c9c6aa', max_length=255),
        ),
    ]
