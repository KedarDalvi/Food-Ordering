# Generated by Django 3.0.6 on 2021-04-12 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210412_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='dict_item',
        ),
    ]
