# Generated by Django 4.2.3 on 2024-09-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_delete_teamuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
