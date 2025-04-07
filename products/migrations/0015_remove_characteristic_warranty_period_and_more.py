# Generated by Django 5.2 on 2025-04-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_characteristic_warranty_period'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characteristic',
            name='warranty_period',
        ),
        migrations.AddField(
            model_name='product',
            name='warranty_period',
            field=models.IntegerField(default=1),
        ),
    ]
