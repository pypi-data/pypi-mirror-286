# Generated by Django 3.2.15 on 2022-10-09 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bpp", "0331_kierunek_studiow"),
    ]

    operations = [
        migrations.AddField(
            model_name="uczelnia",
            name="pbn_api_afiliacja_zawsze_na_uczelnie",
            field=models.BooleanField(
                default=False,
                help_text="Jeżeli praca jest w jednostce z wypełnionym PBN UID bądź w jednostce innej-niż-obca, zatrudniającej-pracowników, to zaznaczenie tej opcji spowoduje, ze  zamiast PBN UID tej jednostki zostanie użyty PBN UID uczelni, co efektywnie spowoduje, że afiliacje w PBN będą na uczelnię, nie zaś na konkretną jednostkę. ",
                verbose_name="Wysyłaj zawsze PBN UID uczelni jako afiliację",
            ),
        ),
    ]
