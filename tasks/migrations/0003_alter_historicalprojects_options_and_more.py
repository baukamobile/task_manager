# Generated by Django 5.1.6 on 2025-03-17 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_status_user_status_project'),
        ('users', '0032_remove_company_has_admin_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalprojects',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Project', 'verbose_name_plural': 'historical Projects'},
        ),
        migrations.AlterModelOptions(
            name='historicaltask',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Task', 'verbose_name_plural': 'historical Tasks'},
        ),
        migrations.AlterModelOptions(
            name='priority',
            options={'verbose_name': 'Priority', 'verbose_name_plural': 'Priorities'},
        ),
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Statuses'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-start_date'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AddField(
            model_name='historicaltask',
            name='project',
            field=models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tasks.projects'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.projects'),
        ),
        migrations.AlterField(
            model_name='historicaltask',
            name='status',
            field=models.ForeignKey(blank=True, db_constraint=False, default=1, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='tasks.status'),
        ),
        migrations.AlterField(
            model_name='priority',
            name='priority_name',
            field=models.CharField(blank=True, choices=[('LOW', 'НИЗКИЙ'), ('MEDIUM', 'СРЕДНИЙ'), ('HIGH', 'ВЫСОКИЙ'), ('CRITICAL', 'КРИТИЧЕСКИЙ'), ('TECHNICAL_DEBT', 'ТЕХНИЧЕСКИЙ ДОЛГ')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.department'),
        ),
        migrations.AlterField(
            model_name='status',
            name='project',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='tasks.projects'),
        ),
        migrations.AlterField(
            model_name='task',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='users.department'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.status'),
        ),
    ]
