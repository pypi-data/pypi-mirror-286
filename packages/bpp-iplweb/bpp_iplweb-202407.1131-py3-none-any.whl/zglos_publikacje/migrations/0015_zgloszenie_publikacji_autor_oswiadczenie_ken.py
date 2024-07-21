# Generated by Django 3.2.16 on 2023-01-29 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zglos_publikacje", "0014_zgloszenie_publikacji_autor_kierunek_studiow"),
    ]

    operations = [
        migrations.AddField(
            model_name="zgloszenie_publikacji_autor",
            name="oswiadczenie_ken",
            field=models.BooleanField(
                blank=True,
                default=None,
                help_text="Oświadczenie Komisji Ewaluacji Nauki (Uniwersytet Medyczny w Lublinie)",
                null=True,
                verbose_name="Oświadczenie KEN",
            ),
        ),
    ]
