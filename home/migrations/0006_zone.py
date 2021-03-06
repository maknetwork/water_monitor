# Generated by Django 3.0.5 on 2020-04-13 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200412_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('name', models.CharField(max_length=250, unique=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='device_zone', serialize=False, to='home.Device')),
                ('gpio', models.CharField(max_length=2, unique=True)),
                ('min_moisture', models.IntegerField()),
                ('time_period', models.TimeField(blank=True, null=True)),
                ('setupcompleted', models.BooleanField(default=False)),
            ],
        ),
    ]
