# Generated by Django 4.2.4 on 2023-09-28 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0021_alter_assigngrampanchayat_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigngrampanchayat',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.staff'),
        ),
    ]
