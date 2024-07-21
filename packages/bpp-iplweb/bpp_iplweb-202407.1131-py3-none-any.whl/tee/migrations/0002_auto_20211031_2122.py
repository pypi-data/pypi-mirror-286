# Generated by Django 3.0.14 on 2021-10-31 20:22

from django.db import migrations, models

import django.contrib.postgres.fields.jsonb


class Migration(migrations.Migration):

    dependencies = [
        ("tee", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="log",
            name="exitcode",
        ),
        migrations.AddField(
            model_name="log",
            name="exit_code",
            field=models.SmallIntegerField(
                blank=True,
                help_text="If value returned by\n    django.core.management.call_command is None, this will be zero. If value returned by d.c.m.call_command\n    is an int, this will be that int. If different, this is set to -1 and exit_value field is set. ",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="log",
            name="exit_value",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True,
                help_text="JSON-encoded value, returned by\n    django.core.management.call_command function, if different than None or an int. ",
                null=True,
            ),
        ),
    ]
