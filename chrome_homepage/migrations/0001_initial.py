# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('thumbnail', filer.fields.image.FilerImageField(to='filer.Image', max_length=5000)),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Websites',
            },
        ),
    ]
