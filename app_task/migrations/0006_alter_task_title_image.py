# Generated by Django 4.2.3 on 2024-09-22 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_task', '0005_task_title_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title_image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
    ]
