# Generated by Django 5.1.6 on 2025-03-04 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0038_remove_historicaltask_tags_remove_task_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltask_comments',
            name='created_at',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='task_comments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
