# Generated by Django 4.0.1 on 2023-07-20 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0026_avaries_depot'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaries',
            name='modifie_par',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modifie_par_avar', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='avaries',
            name='modilfié_le',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='avaries',
            name='saisie_par',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='saisie_par_avar', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
