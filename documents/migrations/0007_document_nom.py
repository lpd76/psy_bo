# Generated by Django 3.0.3 on 2020-09-16 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_auto_20200915_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='nom',
            field=models.CharField(default='master', max_length=100),
            preserve_default=False,
        ),
    ]