from django.apps import AppConfig


class FormRequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'form_requests'

    def ready(self):
        import form_requests.signals
