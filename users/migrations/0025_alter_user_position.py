# Generated by Django 5.1.5 on 2025-02-18 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_alter_roles_options_alter_user_role_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='users.positions'),
        ),
    ]
