# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-06 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_viewnums'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ViewNums',
            new_name='ViewNum',
        ),
        migrations.RemoveField(
            model_name='post',
            name='read_num',
        ),
    ]
