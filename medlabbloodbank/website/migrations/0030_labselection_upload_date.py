# Generated by Django 4.2.4 on 2023-10-04 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0029_donor_timestamp_donorresponse_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='labselection',
            name='upload_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
