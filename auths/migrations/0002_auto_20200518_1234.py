# Generated by Django 3.0.6 on 2020-05-18 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='cinsiyet',
            new_name='sex',
        ),
    ]
