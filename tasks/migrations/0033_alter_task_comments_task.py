# Generated by Django 5.1.5 on 2025-02-21 10:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0032_historicalprojects_assigned_projects_assigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_comments',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='tasks.task'),
        ),
    ]
