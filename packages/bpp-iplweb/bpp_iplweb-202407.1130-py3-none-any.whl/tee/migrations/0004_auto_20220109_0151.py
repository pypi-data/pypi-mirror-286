# Generated by Django 3.0.14 on 2022-01-09 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tee", "0003_log_traceback"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="log",
            name="exit_code",
        ),
        migrations.RemoveField(
            model_name="log",
            name="exit_value",
        ),
        migrations.RemoveField(
            model_name="log",
            name="kwargs",
        ),
        migrations.AddField(
            model_name="log",
            name="finished_successfully",
            field=models.NullBooleanField(),
        ),
    ]
