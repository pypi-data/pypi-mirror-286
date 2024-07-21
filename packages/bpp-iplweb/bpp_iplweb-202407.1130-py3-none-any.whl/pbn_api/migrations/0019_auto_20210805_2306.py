# Generated by Django 3.0.14 on 2021-08-05 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pbn_api", "0018_auto_20210714_0104"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="doi",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publication",
            name="isbn",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publication",
            name="publicUri",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publication",
            name="title",
            field=models.TextField(blank=True, db_index=True, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="institution",
            name="addressCity",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="addressPostalCode",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="addressStreet",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="addressStreetNumber",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="name",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="institution",
            name="polonUid",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="journal",
            name="eissn",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="journal",
            name="issn",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="journal",
            name="mniswId",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="journal",
            name="title",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="journal",
            name="websiteLink",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publication",
            name="year",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publisher",
            name="mniswId",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="publisher",
            name="publisherName",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="lastName",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="name",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="orcid",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="pbnId",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="polonUid",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="scientist",
            name="qualifications",
            field=models.TextField(blank=True, null=True, verbose_name="Tytuł"),
        ),
    ]
