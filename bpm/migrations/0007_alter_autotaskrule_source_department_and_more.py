# Generated by Django 5.1.6 on 2025-04-01 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpm', '0006_alter_workflowstep_process'),
        ('users', '0033_alter_historicaluser_email_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autotaskrule',
            name='source_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_rules', to='users.department'),
        ),
        migrations.AlterField(
            model_name='autotaskrule',
            name='target_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_rules', to='users.department'),
        ),
        migrations.AlterField(
            model_name='dashboardwidget',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dashboardwidget',
            name='width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='process',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processes', to='users.department'),
        ),
        migrations.AlterField(
            model_name='userdepartmentrole',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_roles', to='users.department'),
        ),
    ]
