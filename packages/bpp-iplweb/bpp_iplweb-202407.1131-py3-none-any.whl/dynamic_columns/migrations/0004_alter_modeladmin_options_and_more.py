# Generated by Django 4.2.8 on 2023-12-09 20:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("dynamic_columns", "0001_initial_squashed_0003_modeladmin_model_ref"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="modeladmin",
            options={
                "ordering": ("class_name",),
                "verbose_name": "Model admin",
                "verbose_name_plural": "Model admins",
            },
        ),
        migrations.AlterModelOptions(
            name="modeladmincolumn",
            options={
                "ordering": ("parent", "ordering"),
                "verbose_name": "Model admin column",
                "verbose_name_plural": "Model admin columns",
            },
        ),
        migrations.AlterField(
            model_name="modeladmin",
            name="model_ref",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
        migrations.AlterField(
            model_name="modeladmincolumn",
            name="col_name",
            field=models.CharField(max_length=255, verbose_name="Column name"),
        ),
        migrations.AlterField(
            model_name="modeladmincolumn",
            name="enabled",
            field=models.BooleanField(default=True, verbose_name="Enabled"),
        ),
        migrations.AlterField(
            model_name="modeladmincolumn",
            name="ordering",
            field=models.PositiveSmallIntegerField(verbose_name="Ordering"),
        ),
        migrations.AlterField(
            model_name="modeladmincolumn",
            name="parent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="dynamic_columns.modeladmin",
                verbose_name="Parent",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="modeladmin",
            unique_together={("class_name", "model_ref")},
        ),
    ]
