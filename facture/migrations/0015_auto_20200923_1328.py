# Generated by Django 3.0.3 on 2020-09-23 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facture', '0014_auto_20200923_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestationdeservice',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='prestationdeservice',
            name='qte',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
