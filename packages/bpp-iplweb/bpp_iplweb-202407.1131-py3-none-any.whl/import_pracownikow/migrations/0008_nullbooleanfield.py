# Generated by Django 3.2.14 on 2022-07-08 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("import_pracownikow", "0007_django32"),
    ]

    operations = [
        migrations.AlterField(
            model_name="importpracownikowrow",
            name="podstawowe_miejsce_pracy",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
