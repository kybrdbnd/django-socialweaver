# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_detail', '0005_remove_imagemodel_cropping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='image',
            field=models.ImageField(default='package/no-image.png', upload_to='event'),
        ),
    ]
