# Generated by Django 4.2.4 on 2023-09-07 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_donor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='registration_date',
        ),
    ]
