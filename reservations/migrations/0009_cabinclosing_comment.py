# Generated by Django 2.1.5 on 2019-02-28 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_cabinclosing'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabinclosing',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]