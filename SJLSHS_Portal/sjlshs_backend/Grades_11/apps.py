from django.apps import AppConfig


class Grades11Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Grades_11'

    def ready(self):
        import Grades_11.signals
