# Generated by Django 5.1.6 on 2025-02-25 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email_address', models.EmailField(max_length=254)),
                ('address', models.TextField(max_length=500)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
