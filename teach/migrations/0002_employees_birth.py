# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-04-12 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teach', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='birth',
            field=models.DateField(default='2020-01-01'),
        ),
    ]
