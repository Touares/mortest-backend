# Generated by Django 4.0.1 on 2023-07-21 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_alter_produitdepot_produit'),
    ]

    operations = [
        migrations.AddField(
            model_name='produitachatcommandefournisseur',
            name='prix_achat_produit',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]