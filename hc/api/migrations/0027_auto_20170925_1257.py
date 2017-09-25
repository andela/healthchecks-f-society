# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 12:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='reverse_grace',
            field=models.DurationField(default=datetime.timedelta(0, 3600)),
        ),
        migrations.AddField(
            model_name='check',
            name='running_early',
            field=models.BooleanField(default=False),
        ),
    ]
