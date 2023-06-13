from rest_framework import viewsets
from api.permissions import AdminOrReadOnly
from api.serializers import BooksSerializer
from book.models import Book


class BooksViewSet(viewsets.ModelViewSet):
    serializer_class = BooksSerializer
    permission_classes = (AdminOrReadOnly,)
    queryset = Book.objects.all()
