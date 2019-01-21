# Generated by Django 2.1.5 on 2019-01-21 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cabin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('size', models.IntegerField()),
                ('member_price', models.FloatField()),
                ('non_member_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cabin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_items', to='reservations.Cabin')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_number', models.TextField()),
                ('name', models.TextField()),
                ('phone', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('should_pay', models.BooleanField()),
                ('is_payed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='meta_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_items', to='reservations.ReservationMetaData'),
        ),
    ]
