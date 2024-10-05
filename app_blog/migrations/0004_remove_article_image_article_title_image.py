# Generated by Django 4.2.3 on 2024-09-22 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0003_article_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.AddField(
            model_name='article',
            name='title_image',
            field=models.ImageField(blank=True, null=True, upload_to='article_images/'),
        ),
    ]