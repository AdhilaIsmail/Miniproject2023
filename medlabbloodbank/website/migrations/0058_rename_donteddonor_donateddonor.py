# Generated by Django 4.2.4 on 2023-10-19 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0057_donteddonor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DontedDonor',
            new_name='DonatedDonor',
        ),
    ]