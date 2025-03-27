from django.apps import AppConfig


class MoviesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'moviesapp'

    def ready(self):
        from .signals import create_profile, save_profile



