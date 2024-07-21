# Generated by Django 5.0.3 on 2024-03-31 12:31
import django.contrib.postgres.indexes
from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notification", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddIndex(
            model_name="notification",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["created_at"], name="notification_created_at_idx"),
        ),
        migrations.AddIndex(
            model_name="notification",
            index=django.contrib.postgres.indexes.BTreeIndex(fields=["updated_at"], name="notification_updated_at_idx"),
        ),
        migrations.AddIndex(
            model_name="notificationuser",
            index=django.contrib.postgres.indexes.BTreeIndex(
                fields=["created_at"], name="notificationuser_created_at_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="notificationuser",
            index=django.contrib.postgres.indexes.BTreeIndex(
                fields=["updated_at"], name="notificationuser_updated_at_idx"
            ),
        ),
    ]
