# Generated by Django 5.1.4 on 2024-12-24 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboards', '0011_remove_course_resources'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='resources',
            new_name='resource_link',
        ),
        migrations.AddField(
            model_name='module',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='module_resources/'),
        ),
    ]
