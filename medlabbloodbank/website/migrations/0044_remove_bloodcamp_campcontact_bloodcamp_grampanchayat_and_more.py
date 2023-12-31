# Generated by Django 4.2.4 on 2023-10-08 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0043_bloodcamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodcamp',
            name='campContact',
        ),
        migrations.AddField(
            model_name='bloodcamp',
            name='gramPanchayat',
            field=models.CharField(default='DefaultPanchayat', max_length=100),
        ),
        migrations.AddField(
            model_name='bloodcamp',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bloodcamp',
            name='organizedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.staff'),
        ),
    ]
