# Generated by Django 5.2 on 2025-04-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_characteristic_warranty_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristic',
            name='warranty_period',
            field=models.IntegerField(default=1, editable=False),
        ),
    ]
