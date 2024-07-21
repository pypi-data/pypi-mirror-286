# Generated by Django 2.1.7 on 2019-09-10 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpp', '0178_auto_20190905_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='patent',
            name='tekst_po_ostatnim_autorze',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patent',
            name='tekst_przed_pierwszym_autorem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='praca_doktorska',
            name='tekst_po_ostatnim_autorze',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='praca_doktorska',
            name='tekst_przed_pierwszym_autorem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='praca_habilitacyjna',
            name='tekst_po_ostatnim_autorze',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='praca_habilitacyjna',
            name='tekst_przed_pierwszym_autorem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wydawnictwo_ciagle',
            name='tekst_po_ostatnim_autorze',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wydawnictwo_ciagle',
            name='tekst_przed_pierwszym_autorem',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wydawnictwo_zwarte',
            name='tekst_po_ostatnim_autorze',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='wydawnictwo_zwarte',
            name='tekst_przed_pierwszym_autorem',
            field=models.TextField(blank=True, null=True),
        ),
    ]
