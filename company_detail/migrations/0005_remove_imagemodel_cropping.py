# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 05:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company_detail', '0004_eventmodel_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemodel',
            name='cropping',
        ),
    ]