# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-09 10:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('import_dyscyplin', '0003_auto_20180409_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='import_dyscyplin_row',
            old_name='autor_id',
            new_name='autor',
        ),
        migrations.RenameField(
            model_name='import_dyscyplin_row',
            old_name='jednostka_id',
            new_name='jednostka',
        ),
        migrations.RenameField(
            model_name='import_dyscyplin_row',
            old_name='wydzial_id',
            new_name='wydzial',
        ),
    ]
