# Generated by Django 4.0.1 on 2023-07-20 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_produitdepot_produit_unite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produitdepot',
            name='produit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depotProduit', to='core.produit'),
        ),
    ]