# Generated by Django 5.1.6 on 2025-04-10 06:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpm', '0013_alter_processstagetemplate_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processes', to='bpm.processtemplate'),
        ),
    ]
