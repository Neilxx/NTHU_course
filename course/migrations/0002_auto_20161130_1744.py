# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-30 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='experiences',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.TextField(),
        ),
    ]
