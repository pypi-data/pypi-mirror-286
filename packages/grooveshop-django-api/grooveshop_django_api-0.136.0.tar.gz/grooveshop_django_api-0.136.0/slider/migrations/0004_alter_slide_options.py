# Generated by Django 5.0.4 on 2024-04-11 17:27
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("slider", "0003_alter_slide_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="slide",
            options={
                "ordering": ["sort_order"],
                "verbose_name": "Slide",
                "verbose_name_plural": "Slides",
            },
        ),
    ]
