# Generated by Django 2.2.1 on 2019-05-29 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_polygon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polygon',
            old_name='Provider',
            new_name='provider',
        ),
    ]