# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('server_name', models.CharField(max_length=250)),
                ('head', models.TextField(null=True, blank=True)),
                ('neck', models.TextField(null=True, blank=True)),
                ('back', models.TextField(null=True, blank=True)),
                ('chest', models.TextField(null=True, blank=True)),
                ('wrist', models.TextField(null=True, blank=True)),
                ('hands', models.TextField(null=True, blank=True)),
                ('waist', models.TextField(null=True, blank=True)),
                ('legs', models.TextField(null=True, blank=True)),
                ('feet', models.TextField(null=True, blank=True)),
                ('finger1', models.TextField(null=True, blank=True)),
                ('finger2', models.TextField(null=True, blank=True)),
                ('trinket1', models.TextField(null=True, blank=True)),
                ('trinket2', models.TextField(null=True, blank=True)),
                ('mainHand', models.TextField(null=True, blank=True)),
                ('artifactTraits', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
