# Generated by Django 4.1.3 on 2022-12-02 14:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0003_note_owner_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 2, 19, 57, 20, 129754)),
        ),
    ]
