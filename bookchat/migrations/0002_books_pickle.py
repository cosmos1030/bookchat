# Generated by Django 4.2.3 on 2023-07-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookchat", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="books",
            name="pickle",
            field=models.FileField(default=1, upload_to="uploads/pickles"),
            preserve_default=False,
        ),
    ]