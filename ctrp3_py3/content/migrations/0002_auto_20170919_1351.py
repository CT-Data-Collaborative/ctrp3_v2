# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-19 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='end',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='start',
            field=models.DateField(blank=True, null=True),
        ),
    ]
