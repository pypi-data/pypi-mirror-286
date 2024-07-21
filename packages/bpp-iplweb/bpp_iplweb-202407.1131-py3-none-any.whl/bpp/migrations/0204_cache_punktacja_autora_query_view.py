# Generated by Django 2.2.10 on 2020-03-15 19:40

from django.db import migrations

from bpp.migration_util import load_custom_sql


class Migration(migrations.Migration):

    dependencies = [
        ("bpp", "0203_auto_20200315_2021"),
    ]

    operations = [
        migrations.RunPython(
            lambda *args, **kw: load_custom_sql(
                "0204_cache_punktacja_autora_query_view"
            )
        )
    ]
