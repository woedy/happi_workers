# Generated by Django 4.2.5 on 2023-09-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_time_zone"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="availability_interval",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1 hour", "1 hour"),
                    ("6 hour", "6 hour"),
                    ("24 hour", "24 hour"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]