# Generated by Django 3.0.3 on 2020-09-11 12:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_service_desc'),
        ('facture', '0004_facturable_facture'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrestationDeService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('qte', models.SmallIntegerField()),
                ('prix', models.SmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='facture',
            name='status',
            field=models.CharField(choices=[('PA', 'Payé'), ('RU', 'En cours'), ('OD', 'En retard'), ('PE', 'En attente')], default='PE', max_length=2),
        ),
        migrations.DeleteModel(
            name='Facturable',
        ),
        migrations.AddField(
            model_name='prestationdeservice',
            name='facture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facture.Facture'),
        ),
        migrations.AddField(
            model_name='prestationdeservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Service'),
        ),
    ]
