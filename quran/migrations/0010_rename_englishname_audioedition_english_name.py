# Generated by Django 5.0.6 on 2025-01-07 23:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0009_verse_selected_audio_alter_hostedverseaudio_verse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audioedition',
            old_name='englishName',
            new_name='english_name',
        ),
    ]
