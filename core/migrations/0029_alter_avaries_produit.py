# Generated by Django 4.0.1 on 2023-07-20 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_produitdepot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaries',
            name='produit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.produit'),
        ),
    ]
