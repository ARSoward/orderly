# Generated by Django 2.0 on 2018-01-01 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_orderitem_filled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='requested_delivery',
            field=models.DateField(default=datetime.date(2018, 1, 8), verbose_name='requested delivery date'),
        ),
    ]
