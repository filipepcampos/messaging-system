# Generated by Django 5.1.3 on 2024-11-10 17:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0002_contact"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="GroupChannel",
            new_name="Channel",
        ),
    ]