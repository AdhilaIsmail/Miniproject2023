# Generated by Django 4.2.4 on 2023-10-05 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0031_remove_labselection_upload_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalregister',
            name='gpsCoordinates',
        ),
    ]