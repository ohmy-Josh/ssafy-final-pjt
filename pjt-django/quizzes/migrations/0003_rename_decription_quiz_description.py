# Generated by Django 3.2.12 on 2022-05-24 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0002_auto_20220524_1045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='decription',
            new_name='description',
        ),
    ]
