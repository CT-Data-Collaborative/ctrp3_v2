# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-20 14:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_homepage_teaser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepage',
            name='teaser',
        ),
    ]