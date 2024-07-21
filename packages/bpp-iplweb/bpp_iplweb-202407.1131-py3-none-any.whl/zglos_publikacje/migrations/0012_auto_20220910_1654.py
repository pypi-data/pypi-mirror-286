# Generated by Django 3.2.15 on 2022-09-10 14:54

import django.db.models.deletion
import django.db.models.manager
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bpp", "0327_uczelnia_pokazuj_formularz_zglaszania_publikacji"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("zglos_publikacje", "0011_auto_20220910_1646"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="obslugujacy_zgloszenia_wydzialow",
            managers=[
                ("manager", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name="obslugujacy_zgloszenia_wydzialow",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Użytkownik",
            ),
        ),
        migrations.AlterField(
            model_name="obslugujacy_zgloszenia_wydzialow",
            name="wydzial",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bpp.wydzial",
                verbose_name="Wydział",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="obslugujacy_zgloszenia_wydzialow",
            unique_together={("user", "wydzial")},
        ),
    ]
