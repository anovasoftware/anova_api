# Generated by Django 5.1.5 on 2025-04-11 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bridge', '0002_rename_natonality_manifest_nationality'),
        ('static', '0008_hotel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manifest',
            name='hotel',
            field=models.ForeignKey(default='A000', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='static.hotel'),
        ),
    ]
