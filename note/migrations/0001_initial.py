# Generated by Django 3.0.3 on 2020-09-16 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0014_auto_20200915_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('note', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Client')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='note.NoteType')),
            ],
        ),
    ]
