# Generated by Django 4.2.4 on 2023-09-19 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('blood_group', models.CharField(max_length=5)),
                ('purpose', models.TextField()),
            ],
        ),
    ]
