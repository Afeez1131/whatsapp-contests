# Generated by Django 3.2 on 2022-09-13 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='guest_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]