# Generated by Django 2.1.5 on 2019-02-02 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0031_auto_20190131_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image'),
        ),
    ]
