# Generated by Django 4.0.1 on 2022-01-21 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room_booking_app', '0002_room_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_booking_app.room')),
            ],
            options={
                'unique_together': {('room_id', 'date')},
            },
        ),
    ]
