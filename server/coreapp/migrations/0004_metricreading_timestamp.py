# Generated by Django 5.1.7 on 2025-03-07 21:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coreapp", "0003_metric_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="metricreading",
            name="timestamp",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 3, 7, 21, 8, 59, 925597, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
    ]
