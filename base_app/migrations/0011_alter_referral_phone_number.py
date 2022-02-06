# Generated by Django 3.2 on 2022-02-06 07:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0010_alter_referral_refer_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='phone_number',
            field=models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2348105506070'. Up to 14 digits allowed.", regex='^[+]\\d{13}$')]),
        ),
    ]
