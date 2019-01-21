# Generated by Django 2.1.5 on 2019-01-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationmetadata',
            old_name='is_payed',
            new_name='is_paid',
        ),
        migrations.AddField(
            model_name='reservation',
            name='members',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='non_members',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
