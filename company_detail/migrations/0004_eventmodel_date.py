# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 10:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_detail', '0003_reviewmodel_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
