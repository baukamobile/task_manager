# Generated by Django 5.1.6 on 2025-02-26 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0033_alter_task_comments_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaltask',
            name='agreed_with_managers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='agreed_with_managers',
            field=models.BooleanField(default=False),
        ),
    ]
