# Generated by Django 4.2.4 on 2023-10-06 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_remove_uploadedfile_selected_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodCamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camp_date', models.DateField()),
                ('camp_name', models.CharField(max_length=255)),
                ('camp_address', models.TextField()),
                ('camp_district', models.CharField(max_length=255)),
                ('camp_contact', models.CharField(max_length=20)),
                ('conducted_by', models.CharField(max_length=255)),
                ('register', models.CharField(max_length=255)),
                ('camp_time', models.TimeField()),
                ('organized_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.staff')),
            ],
        ),
    ]
