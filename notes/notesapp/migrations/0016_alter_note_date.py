# Generated by Django 4.1.4 on 2022-12-16 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0015_note_uploadedfile_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 16, 14, 46, 5, 852036)),
        ),
    ]
