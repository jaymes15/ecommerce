# Generated by Django 2.1.5 on 2019-01-28 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0021_auto_20190128_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
