# Generated by Django 2.1.5 on 2019-01-28 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0018_cartitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='Product_image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='Product_image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='Product_image4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
