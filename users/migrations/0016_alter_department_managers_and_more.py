# Generated by Django 5.1.5 on 2025-02-13 09:10

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_department_deacivate'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='department',
            managers=[
                ('activate', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='department',
            old_name='deacivate',
            new_name='deactivate',
        ),
    ]
