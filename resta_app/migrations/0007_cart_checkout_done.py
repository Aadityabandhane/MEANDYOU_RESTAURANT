# Generated by Django 5.1.1 on 2025-01-11 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resta_app', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='checkout_done',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
