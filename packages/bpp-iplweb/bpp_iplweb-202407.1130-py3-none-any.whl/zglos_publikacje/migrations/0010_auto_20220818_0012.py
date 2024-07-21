# Generated by Django 3.2.15 on 2022-08-17 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zglos_publikacje", "0009_alter_zgloszenie_publikacji_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="zgloszenie_publikacji",
            options={
                "ordering": ("-ostatnio_zmieniony", "tytul_oryginalny"),
                "verbose_name": "zgłoszenie publikacji",
                "verbose_name_plural": "zgłoszenia publikacji",
            },
        ),
        migrations.AddField(
            model_name="zgloszenie_publikacji",
            name="rodzaj_zglaszanej_publikacji",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "artykuł naukowy lub monografia"),
                    (2, "pozostałe rodzaje"),
                ],
                default=1,
                help_text="Dla artykułów naukowych i monografii konieczne będzie wprowadzenie "
                "informacji o kosztach w ostatnim etapie wypełniania formularza. ",
                verbose_name="Rodzaj zgłaszanej publikacji",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="zgloszenie_publikacji",
            name="kod_do_edycji",
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
    ]
