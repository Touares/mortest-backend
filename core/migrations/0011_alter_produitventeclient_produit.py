# Generated by Django 4.0.1 on 2023-07-04 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_vendeur_adress_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produitventeclient',
            name='produit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='produit_vente_client', to='core.produit'),
        ),
    ]