# Generated by Django 5.1.5 on 2025-02-18 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryimage',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
