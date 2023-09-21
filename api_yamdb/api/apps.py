from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        from api.views import code_generated
        from api.signals import send_code

        code_generated.connect(send_code)
