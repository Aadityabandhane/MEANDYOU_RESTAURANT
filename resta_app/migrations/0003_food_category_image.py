# Generated by Django 5.1.1 on 2024-11-04 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resta_app', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
