# Generated by Django 3.0.3 on 2020-09-15 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20200915_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]
