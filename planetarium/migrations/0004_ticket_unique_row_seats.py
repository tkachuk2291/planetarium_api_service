# Generated by Django 5.0.4 on 2024-05-01 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0003_alter_showsession_show_time'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.UniqueConstraint(fields=('row', 'seat'), name='unique_row_seats'),
        ),
    ]
