# Generated by Django 4.2.4 on 2023-10-09 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0044_remove_bloodcamp_campcontact_bloodcamp_grampanchayat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='approval_status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]