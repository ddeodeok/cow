# Generated by Django 3.2.12 on 2022-09-26 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cow', '0010_cow_pregnancy_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cow',
            name='pregnancy_date',
        ),
    ]