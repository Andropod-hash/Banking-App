# Generated by Django 4.2.1 on 2023-12-17 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_kyc_identify_image_alter_kyc_identify_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]
