# Generated by Django 3.0.3 on 2020-09-14 17:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0007_auto_20200914_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facture',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='prestationdeservice',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
