# Generated by Django 3.2.8 on 2021-10-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_attendance_attended_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='attendance_taking_status',
        ),
        migrations.AddField(
            model_name='course',
            name='attendance_taking_status',
            field=models.BooleanField(default=False),
        ),
    ]
