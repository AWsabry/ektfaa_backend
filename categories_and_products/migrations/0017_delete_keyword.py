# Generated by Django 4.2.7 on 2023-11-07 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("categories_and_products", "0016_alter_keyword_product"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Keyword",
        ),
    ]