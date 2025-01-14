# Generated by Django 4.2.3 on 2024-08-08 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50)),
                ('members', models.TextField(max_length=100)),
                ('points', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль команды',
                'verbose_name_plural': 'Профили команд',
                'ordering': ['created'],
                'permissions': (('status_team', 'user_get_status_team'),),
            },
        ),
        migrations.CreateModel(
            name='SingleUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('profession', models.CharField(blank=True, max_length=50, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='profile_images/default.jpg', null=True, upload_to='profile_images')),
                ('level', models.CharField(default='Beginner', max_length=10)),
                ('points', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
                'ordering': ['created'],
            },
        ),
    ]
