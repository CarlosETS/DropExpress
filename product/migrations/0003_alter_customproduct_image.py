# Generated by Django 4.2.6 on 2023-12-09 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_customproduct_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customproduct',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]