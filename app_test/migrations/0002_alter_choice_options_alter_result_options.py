# Generated by Django 4.2.3 on 2024-08-08 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'verbose_name': 'Выбор пользователя', 'verbose_name_plural': 'Выборы пользователей'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'Результат', 'verbose_name_plural': 'Результаты'},
        ),
    ]
