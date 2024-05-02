# Generated by Django 5.0.4 on 2024-05-02 12:04

import planetarium.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0007_planetariumdome_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='astronomyshow',
            name='image',
            field=models.ImageField(null=True, upload_to=planetarium.models.image_path),
        ),
    ]