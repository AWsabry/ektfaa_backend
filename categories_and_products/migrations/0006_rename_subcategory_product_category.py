# Generated by Django 4.2.6 on 2023-10-20 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories_and_products', '0005_alter_product_subcategory_delete_subcategory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='subCategory',
            new_name='category',
        ),
    ]
