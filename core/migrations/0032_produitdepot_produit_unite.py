# Generated by Django 4.0.1 on 2023-07-20 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_produitdepot_produit_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='produitdepot',
            name='produit_unite',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]