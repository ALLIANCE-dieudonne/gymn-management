# Generated by Django 5.1.2 on 2024-10-27 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authapp", "0003_enroll_duedate_enroll_paymentstatus_enroll_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="enroll",
            old_name="trainer",
            new_name="trainers",
        ),
    ]
