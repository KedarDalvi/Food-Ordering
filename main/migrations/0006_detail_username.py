# Generated by Django 3.0.6 on 2021-04-12 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210412_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='username',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]