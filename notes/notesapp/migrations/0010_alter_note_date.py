# Generated by Django 4.1.3 on 2022-12-06 15:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0009_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 6, 20, 16, 29, 555595)),
        ),
    ]
