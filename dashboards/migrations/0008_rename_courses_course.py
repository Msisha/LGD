# Generated by Django 5.1.4 on 2024-12-21 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboards', '0007_alter_trainingrequest_status_courses'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='courses',
            new_name='course',
        ),
    ]
