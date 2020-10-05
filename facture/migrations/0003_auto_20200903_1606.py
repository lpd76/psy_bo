# Generated by Django 3.0.3 on 2020-09-03 20:06

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200903_1447'),
        ('facture', '0002_auto_20200903_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Client')),
                ('psychologue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Psychologue')),
            ],
        ),
#         migrations.AddField(
#             model_name='facturable',
#             name='facture',
#             field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='facture.Facture'),
#             preserve_default=False,
#         ),
    ]
