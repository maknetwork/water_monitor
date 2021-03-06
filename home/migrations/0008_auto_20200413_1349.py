# Generated by Django 3.0.5 on 2020-04-13 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200413_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='last_active_measured',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zone',
            name='last_active_moisture',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='zone',
            name='last_measured',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='zone',
            name='last_measured_moisture',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
