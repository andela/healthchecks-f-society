# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_current_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reports_allowed',
            field=models.CharField(default='none', max_length=8),
        ),
    ]