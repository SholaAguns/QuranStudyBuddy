# Generated by Django 5.0.6 on 2024-12-01 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translation',
            name='verse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='quran.verse'),
        ),
    ]
