# Generated by Django 2.1.5 on 2019-01-30 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0026_auto_20190130_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='Product_store',
        ),
    ]
