# Generated by Django 2.1.15 on 2021-01-16 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210115_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='original_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='image',
            name='image_source',
        ),
    ]
