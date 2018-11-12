# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wow_monitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimcRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dps_rank', models.IntegerField()),
                ('rating_time', models.DateTimeField(auto_now_add=True)),
                ('character', models.ForeignKey(to='wow_monitor.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
