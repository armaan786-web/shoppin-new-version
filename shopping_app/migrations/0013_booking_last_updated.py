# Generated by Django 4.1.5 on 2023-01-27 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_app', '0012_withdraw_withdraw_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='last_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
