from django.apps import AppConfig


class AuthorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'author'

class ApplicationConfig(AppConfig):
    name ="author"
    def ready(self):
        from author import receiver