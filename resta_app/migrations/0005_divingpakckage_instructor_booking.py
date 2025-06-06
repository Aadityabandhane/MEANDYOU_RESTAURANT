# Generated by Django 5.1.1 on 2024-11-08 07:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resta_app', '0004_customer_details'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Divingpakckage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tital', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price_per_person', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('experience_years', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('diving_pakckage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resta_app.divingpakckage')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resta_app.instructor')),
            ],
        ),
    ]
