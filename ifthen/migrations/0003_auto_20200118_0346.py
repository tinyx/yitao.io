# Generated by Django 2.2.9 on 2020-01-18 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ifthen', '0002_move_guid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(blank=True, help_text='Loser of the game', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lost_games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, help_text='Winner of the game', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_games', to=settings.AUTH_USER_MODEL),
        ),
    ]
