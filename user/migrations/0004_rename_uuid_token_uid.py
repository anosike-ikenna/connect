# Generated by Django 3.2.5 on 2021-10-23 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='uuid',
            new_name='uid',
        ),
    ]
