# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-30 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_course_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='title',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
