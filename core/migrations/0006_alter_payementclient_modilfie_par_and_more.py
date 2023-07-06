# Generated by Django 4.0.1 on 2023-06-24 14:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_remove_payementclient_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payementclient',
            name='modilfie_par',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modifie_par_pc', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='payementclient',
            name='saisie_par',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saisie_par_pc', to=settings.AUTH_USER_MODEL),
        ),
    ]