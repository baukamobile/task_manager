# Generated by Django 5.1.6 on 2025-03-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_alter_news_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='news_documents'),
        ),
    ]
