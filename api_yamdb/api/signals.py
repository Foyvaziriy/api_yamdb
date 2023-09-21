from django.core.mail import send_mail


def send_code(sender, **kwargs) -> None:
    subject: str = 'Код подтверждения регистрации'
    message: str = f'Ваш код подтверждения: {kwargs.get("confirmation_code")}'
    from_email: str = 'production@yandex.ru'
    recipient_list: list = [kwargs.get('user_email')]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )
