import string
import random
from django.core.mail import send_mail

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()


def generate_confirmation_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


def send_verification_email(to_email, verification_code, user_email=None):
    subject = 'Код подтверждения регистрации'
    message = f'Ваш код подтверждения: {verification_code}'
    recipient_list = [user_email]

    send_mail(subject, message, recipient_list)

    print(f'Письмо сохранено в локальной папке для {to_email}')


def get_tokens_for_user(user: User) -> dict[str, str]:
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
