from book.models import Book
from rest_framework import serializers


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description',)

