# Generated by Django 4.0.6 on 2022-07-26 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_кщду'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='кщду',
            new_name='role',
        ),
    ]
