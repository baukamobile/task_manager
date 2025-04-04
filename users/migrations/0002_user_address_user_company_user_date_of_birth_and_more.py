# Generated by Django 5.1.5 on 2025-02-05 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='on_vacation',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.positions'),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
