# Generated by Django 5.1.6 on 2025-03-19 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('placed', 'placed'), ('out_for_delivery', 'out_for_delivery'), ('in_transit', 'in_transit'), ('delivered', 'delivered')], max_length=100),
        ),
    ]
