# Generated by Django 3.0.3 on 2020-09-11 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_auto_20200911_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='suggested_price',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='unit',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]