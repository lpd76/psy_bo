# Generated by Django 3.0.3 on 2020-09-04 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum_vitae', '0002_auto_20200904_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expérienceprofessionelle',
            name='date_fin',
            field=models.DateField(blank=True, null=True),
        ),
    ]
