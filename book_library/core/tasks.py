from api.send_notification import send_confirmation_code
from api.utils import import_books_cvs
from core.celery import app
from datetime import datetime
from rentals.models import Rentals


@app.task
def check_rentals_users():
    them = 'Срок аренды книг завершился'
    text = (
        '{} Добрый день. Срок аренды книг '
        'завершился. Hеобходимо вернуть: {}'
    )
    rentals = Rentals.objects.filter(
        return_date__date__lte=datetime.today().date()
    ).select_related('reader').prefetch_related('books')
    for rental in rentals:
        books = rental.books.all()
        text = text.format(
            rental.reader,
            ', '.join([book.title for book in books])
        )
        send_confirmation_code(rental, them, text)


@app.task
def upload_data(file):
    import_books_cvs(file)
