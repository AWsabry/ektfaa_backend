# Generated by Django 4.2.7 on 2023-11-09 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories_and_products", "0022_alter_userupload_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="userupload",
            name="serial_number",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]