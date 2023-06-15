from book_library import settings
from django.core.mail import send_mail


def send_confirmation_code(obj, them, text):
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, [obj.reader.email])
    print(f'Сообщение "{text}" отправлено.')
