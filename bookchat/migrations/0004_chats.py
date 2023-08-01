# Generated by Django 4.2.3 on 2023-07-30 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("bookchat", "0003_alter_books_pickle"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chats",
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
                ("book", models.CharField(max_length=50)),
                ("user_msg", models.CharField(max_length=400)),
                ("bot_msg", models.CharField(max_length=400)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
