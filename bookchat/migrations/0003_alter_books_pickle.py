# Generated by Django 4.2.3 on 2023-07-29 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookchat", "0002_books_pickle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="books",
            name="pickle",
            field=models.FileField(blank=True, upload_to="uploads/pickles"),
        ),
    ]
