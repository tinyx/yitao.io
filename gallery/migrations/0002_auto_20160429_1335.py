# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_cn',
            field=models.CharField(default='\u7c7b\u522b', help_text=b'The name of the category', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='description_cn',
            field=models.TextField(help_text=b'The description that will appear under the image', null=True, blank=True),
            preserve_default=True,
        ),
    ]
