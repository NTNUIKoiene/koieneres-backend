# Generated by Django 2.1.5 on 2019-01-29 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_auto_20190129_1421'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='reservation',
            name='reservation_date_737521_brin',
        ),
    ]
