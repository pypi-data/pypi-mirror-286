# Generated by Django 3.2.15 on 2022-10-02 23:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("dynamic_columns", "0001_initial"),
        ("dynamic_columns", "0002_auto_20221002_2252"),
        ("dynamic_columns", "0003_modeladmin_model_ref"),
    ]

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModelAdmin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("class_name", models.TextField()),
                (
                    "model_ref",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ModelAdminColumn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("col_name", models.CharField(max_length=255)),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dynamic_columns.modeladmin",
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("ordering", models.PositiveSmallIntegerField(default=1)),
            ],
            options={
                "unique_together": {("parent", "col_name")},
                "ordering": ("parent", "ordering"),
            },
        ),
    ]
