# Generated by Django 3.0.3 on 2020-09-09 17:56

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200909_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='psychologue',
            name='phone',
            field=phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31),
        ),
    ]
