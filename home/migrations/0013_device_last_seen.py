# Generated by Django 3.0.5 on 2020-04-20 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_device_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='last_seen',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
