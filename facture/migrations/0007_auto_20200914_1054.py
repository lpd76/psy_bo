# Generated by Django 3.0.3 on 2020-09-14 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0006_auto_20200912_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='date',
            field=models.DateField(blank=True, default=datetime.date(2020, 9, 14)),
        ),
    ]
