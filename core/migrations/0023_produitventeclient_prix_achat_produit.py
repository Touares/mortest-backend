# Generated by Django 4.0.1 on 2023-07-14 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_remove_payementfournisseur_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='produitventeclient',
            name='prix_achat_produit',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
