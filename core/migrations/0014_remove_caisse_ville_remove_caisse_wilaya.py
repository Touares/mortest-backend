# Generated by Django 4.0.1 on 2023-07-07 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_rename_prix_datail_produit_produitventeclient_prix_detail_produit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caisse',
            name='ville',
        ),
        migrations.RemoveField(
            model_name='caisse',
            name='wilaya',
        ),
    ]