# Generated by Django 4.0.1 on 2023-07-23 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_payementclient_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='fraisgenerales',
            name='numero',
            field=models.CharField(default='1', max_length=30),
        ),
        migrations.AddField(
            model_name='payementfournisseur',
            name='numero',
            field=models.CharField(default='1', max_length=30),
        ),
    ]
