# Generated by Django 4.2.7 on 2023-12-02 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projectss_review_tag_delete_project_projectss_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Projectss',
            new_name='project',
        ),
    ]
