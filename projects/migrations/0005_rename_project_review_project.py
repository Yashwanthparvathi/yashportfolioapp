# Generated by Django 4.2.7 on 2023-12-07 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_featured_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='project',
            new_name='Project',
        ),
    ]
