# Generated by Django 2.1.8 on 2019-09-25 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_refinery_common", "0040_auto_20190925_2040"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="computedfile",
            index=models.Index(fields=["filename"], name="computed_fi_filenam_64958d_idx"),
        ),
    ]
