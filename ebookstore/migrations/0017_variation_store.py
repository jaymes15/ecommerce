# Generated by Django 2.1.5 on 2019-01-24 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ebookstore', '0016_cartitem_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ebookstore.Stores'),
        ),
    ]