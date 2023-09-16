import string
import random

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


User = get_user_model()


def generate_confirmation_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def send_code(confirmation_code: str, user_email: str) -> None:
    subject: str = 'Код подтверждения регистрации'
    message: str = f'Ваш код подтверждения: {confirmation_code}'
    from_email: str = 'production@yandex.ru'
    recipient_list: list = [user_email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list
    )

    print(f'Письмо сохранено в локальной папке для {user_email}')


def get_tokens_for_user(user: User) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }
