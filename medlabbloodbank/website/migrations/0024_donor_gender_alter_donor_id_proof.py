# Generated by Django 4.2.4 on 2023-10-03 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_donor_id_proof'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donor',
            name='id_proof',
            field=models.FileField(upload_to='id_proofs/'),
        ),
    ]
