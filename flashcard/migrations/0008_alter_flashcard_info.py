# Generated by Django 5.0.6 on 2025-01-19 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0007_flashcard_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='info',
            field=models.TextField(default='', null=True),
        ),
    ]
