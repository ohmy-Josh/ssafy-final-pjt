# Generated by Django 3.2.12 on 2022-05-24 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
        ('quizzes', '0003_rename_decription_quiz_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizplay',
            name='results',
            field=models.ManyToManyField(related_name='results', to='movies.Movie'),
        ),
        migrations.AlterField(
            model_name='quizplay',
            name='answer_list',
            field=models.ManyToManyField(related_name='answers', to='movies.Movie'),
        ),
    ]
