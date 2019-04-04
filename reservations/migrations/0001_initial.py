# Generated by Django 2.1.5 on 2019-01-29 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Cabin',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('article_number', models.IntegerField()),
                ('name', models.TextField()),
                ('size', models.IntegerField()),
                ('member_price', models.FloatField()),
                ('non_member_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('date', models.DateField()),
                ('members', models.IntegerField()),
                ('non_members', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ReservationMetaData',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('membership_number', models.TextField()),
                ('name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('should_pay', models.BooleanField()),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at', ),
            },
        ),
    ]
