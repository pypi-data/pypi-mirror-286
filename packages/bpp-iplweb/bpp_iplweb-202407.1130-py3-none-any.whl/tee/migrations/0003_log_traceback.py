# Generated by Django 3.0.14 on 2021-11-01 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tee", "0002_auto_20211031_2122"),
    ]

    operations = [
        migrations.AddField(
            model_name="log",
            name="traceback",
            field=models.TextField(blank=True, null=True),
        ),
    ]
