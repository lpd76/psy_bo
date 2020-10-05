# Generated by Django 3.0.3 on 2020-09-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0015_auto_20200923_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='facture',
            name='paid_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]