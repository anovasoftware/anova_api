# Generated by Django 5.1.5 on 2025-07-06 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static', '0015_formcontrol'),
    ]

    operations = [
        migrations.AddField(
            model_name='formcontrol',
            name='control_type',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]
