# Generated by Django 2.2.5 on 2019-09-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0010_extendedperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabin',
            name='in_use',
            field=models.BooleanField(default=True),
        ),
    ]
