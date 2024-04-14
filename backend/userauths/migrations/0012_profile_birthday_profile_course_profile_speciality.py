# Generated by Django 5.0.2 on 2024-04-14 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0011_alter_profile_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='course',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='speciality',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]