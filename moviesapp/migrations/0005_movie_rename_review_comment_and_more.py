# Generated by Django 5.1.6 on 2025-03-20 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0004_movierecommendation_year'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('release_year', models.IntegerField(blank=True, null=True)),
                ('genre', models.CharField(blank=True, max_length=100)),
                ('director', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.RenameModel(
            old_name='Review',
            new_name='Comment',
        ),
        migrations.RenameField(
            model_name='movierecommendation',
            old_name='description',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='movierecommendation',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movierecommendation',
            name='title',
        ),
        migrations.RemoveField(
            model_name='movierecommendation',
            name='year',
        ),
        migrations.AddField(
            model_name='movierecommendation',
            name='movie',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='moviesapp.movie', verbose_name='Movie title'),
            preserve_default=False,
        ),
    ]
