# Generated by Django 2.0 on 2017-12-12 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='business',
        ),
        migrations.RemoveField(
            model_name='account',
            name='user',
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
