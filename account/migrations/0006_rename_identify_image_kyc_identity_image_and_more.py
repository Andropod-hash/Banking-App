# Generated by Django 4.2.1 on 2023-12-17 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_kyc_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kyc',
            old_name='identify_image',
            new_name='identity_image',
        ),
        migrations.RenameField(
            model_name='kyc',
            old_name='identify_type',
            new_name='identity_type',
        ),
    ]
