# Generated by Django 3.2.5 on 2021-10-28 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20211025_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='username',
        ),
    ]
