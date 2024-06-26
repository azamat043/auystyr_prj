# Generated by Django 5.0.2 on 2024-02-23 10:44

import userauths.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0003_alter_profile_verified_alter_profile_working_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                default="cover.jpg",
                null=True,
                upload_to=userauths.models.user_directory_path,
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                blank=True,
                default="default.jpg",
                null=True,
                upload_to=userauths.models.user_directory_path,
            ),
        ),
    ]
