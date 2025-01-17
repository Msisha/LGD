# Generated by Django 5.1.4 on 2024-12-23 04:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboards', '0009_remove_course_employees_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='employees',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role__role_name': 'Employee'}, related_name='enrolled_courses', to='authentication.user'),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('module_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('resources', models.URLField(blank=True, max_length=1024, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='dashboards.course')),
            ],
        ),
    ]
