# Generated by Django 4.1.3 on 2022-12-04 10:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesapp', '0007_alter_note_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 4, 15, 26, 7, 240970)),
        ),
    ]
