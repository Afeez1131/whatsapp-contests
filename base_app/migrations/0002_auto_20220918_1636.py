# Generated by Django 3.2 on 2022-09-18 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referral',
            old_name='business_owner',
            new_name='contest',
        ),
        migrations.AlterUniqueTogether(
            name='referral',
            unique_together={('contest', 'refer_name', 'phone_number')},
        ),
    ]
