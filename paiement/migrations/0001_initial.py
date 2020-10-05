# Generated by Django 3.0.3 on 2020-09-17 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0014_auto_20200915_0827'),
        ('facture', '0010_prestationdeservice_qte'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('montant', models.DecimalField(decimal_places=2, max_digits=6)),
                ('type', models.CharField(choices=[('I', 'Interact'), ('R', 'Crédit'), ('M', 'MasterCard'), ('V', 'Visa'), ('C', 'Argent')], default='R', max_length=1)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Client')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facture.Facture')),
            ],
        ),
    ]
