# Generated by Django 3.2 on 2022-02-06 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0011_alter_referral_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='refer_message',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referral_url',
        ),
    ]
