# Generated by Django 4.1.4 on 2022-12-14 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0012_note_isprivate_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 14, 14, 22, 55, 569585)),
        ),
    ]
