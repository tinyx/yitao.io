# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the category', max_length=255)),
                ('order', models.IntegerField(default=0, help_text=b'The order of this category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name of the image', max_length=255)),
                ('description', models.TextField(help_text=b'The description that will appear under the image', null=True, blank=True)),
                ('order', models.IntegerField(default=0, help_text=b'The order of this image under the category')),
                ('annotation', models.TextField(help_text=b'Write something to remind you which image this is', null=True, blank=True)),
                ('category', models.ForeignKey(help_text=b'The category of this image', to='gallery.Category')),
                ('image_file', filer.fields.image.FilerImageField(to='filer.Image', max_length=5000, help_text=b'The image file')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
