# Generated by Django 2.2.7 on 2019-12-25 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newYearGame', '0002_remove_profile_time_fin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='time_fin',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время окончания игры'),
        ),
    ]
