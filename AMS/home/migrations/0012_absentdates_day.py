# Generated by Django 3.2.8 on 2021-10-27 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_absentdates_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='absentdates',
            name='day',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
