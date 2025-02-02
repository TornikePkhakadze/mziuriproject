# Generated by Django 5.1.5 on 2025-02-02 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(related_name='categories', to='products.product'),
        ),
        migrations.AddField(
            model_name='categoryimage',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='categories.category'),
        ),
    ]
