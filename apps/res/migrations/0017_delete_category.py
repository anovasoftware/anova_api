# Generated by Django 5.1.5 on 2025-04-13 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('res', '0016_alter_posmenu_category_alter_room_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]
