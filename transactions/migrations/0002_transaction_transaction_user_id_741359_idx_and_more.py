# Generated by Django 4.2.20 on 2025-04-24 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(
                fields=["user", "-date"], name="transaction_user_id_741359_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="transaction",
            index=models.Index(fields=["date"], name="transaction_date_ad8c94_idx"),
        ),
    ]
