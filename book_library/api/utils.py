import csv
from io import StringIO
from book.models import Book, Genre, Author
from book_library import settings
from django.core.mail import send_mail


def send_notification(obj, them, text):
    email_from = settings.EMAIL_BACKEND
    send_mail(them, text, email_from, [obj.reader.email])
    print(f'Сообщение "{text}" отправлено.')


def import_books_cvs(file):
    reader = csv.DictReader(
        StringIO(file.read().decode('utf8')),
        delimiter=';'
    )
    for idx, row in enumerate(reader, start=2):
        book = row.get('title')
        genre = row.get('genre')
        author = row.get('author')
        remains = row.get('remains') if row.get('remains') else 0
        book_obj, book_create = Book.objects.get_or_create(title=book)

        if genre:
            genre_obj, genre_create = Genre.objects.get_or_create(title=genre)
            book_obj.genre.add(genre_obj)

        if author:
            author = author.split(' ')
            author_obj, author_create = Author.objects.get_or_create(
                first_name=author[0],
                last_name=author[1]
            )
            book_obj.author.add(author_obj)
        book_obj.remains += int(remains)
        book_obj.save()
