# Generated by Django 5.1.6 on 2025-03-28 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0011_alter_profile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='synopsis',
            new_name='overview',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='release_year',
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='tmdb_id',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movierecommendation',
            name='trailer_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
