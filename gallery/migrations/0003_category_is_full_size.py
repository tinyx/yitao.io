# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20160429_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_full_size',
            field=models.BooleanField(default=False, help_text=b'Should this category be rendered full zied.'),
            preserve_default=True,
        ),
    ]
