# Generated by Django 3.2.12 on 2022-09-27 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cow', '0012_cow_pregnancy_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
