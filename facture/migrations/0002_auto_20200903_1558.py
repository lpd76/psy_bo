# Generated by Django 3.0.3 on 2020-09-03 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200903_1447'),
        ('service', '0001_initial'),
        ('facture', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Facture',
            new_name='Facturable',
        ),
    ]
