# Generated by Django 5.0.2 on 2024-02-22 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0002_alter_profile_gender_alter_user_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="verified",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="working_at",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.BooleanField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female")],
                max_length=100,
                null=True,
            ),
        ),
    ]