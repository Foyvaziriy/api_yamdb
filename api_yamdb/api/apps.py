from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        from api.views import send_email
        from users.services import send_code

        send_email.connect(send_code)
