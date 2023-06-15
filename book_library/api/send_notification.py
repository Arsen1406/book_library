from book_library import settings
from django.core.mail import send_mail


def send_confirmation_code(them, text, user):
    # them = 'Срок аренды книг завершился'
    # text = f'Срок аренды книг завершился. Hеобходимо вернуть: {1}'
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, [user.email])
