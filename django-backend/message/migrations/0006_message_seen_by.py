# Generated by Django 5.1.3 on 2024-11-10 18:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0005_alter_channel_start_date_alter_message_sent_date"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="seen_by",
            field=models.ManyToManyField(
                related_name="seen_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
