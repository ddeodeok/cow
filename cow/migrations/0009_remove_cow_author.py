# Generated by Django 3.2.12 on 2022-09-26 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cow', '0008_cow_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cow',
            name='author',
        ),
    ]