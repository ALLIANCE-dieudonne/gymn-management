# Generated by Django 5.1.2 on 2024-10-28 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authapp", "0005_gallery"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phoneNumber", models.CharField(max_length=12)),
                ("selectDate", models.DateField(auto_now_add=True)),
                ("Login", models.CharField(max_length=100)),
                ("logout", models.CharField(max_length=100)),
                ("selectWorkout", models.CharField(max_length=100)),
                ("trainedBy", models.CharField(max_length=100)),
            ],
        ),
    ]