# Generated by Django 4.0.1 on 2023-07-10 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_remove_payementfournisseur_achat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payementfournisseur',
            name='date',
        ),
    ]
