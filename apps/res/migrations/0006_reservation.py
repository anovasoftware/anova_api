# Generated by Django 5.1.5 on 2025-03-21 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_company'),
        ('res', '0005_remove_category_external_id_remove_room_external_id'),
        ('static', '0005_alter_client_parent_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('static_flag', models.CharField(blank=True, default='N', max_length=1)),
                ('internal_comment', models.TextField(blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('hotel', models.ForeignKey(default='A000', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='static.hotel')),
                ('person', models.ForeignKey(default='A00000', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.person')),
                ('status', models.ForeignKey(default='001', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='static.status')),
                ('travel_agency_company', models.ForeignKey(default='A0000', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.company')),
                ('type', models.ForeignKey(default='000', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='static.type')),
            ],
            options={
                'verbose_name_plural': 'reservation table (res_reservation)',
                'db_table': 'res_reservation',
                'ordering': [],
            },
        ),
    ]
