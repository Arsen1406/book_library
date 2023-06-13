from book.models import Book, Genre, Author
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rentals.models import Rentals

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+',
        max_length=150,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        min_length=None,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')
        read_only_fields = ('username', 'password')


class UserSerializer(SignUpSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'description',)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name', 'birth_day')


class BooksSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'description',
            'genre',
            'remains',
        )


class RentalsSerializer(serializers.ModelSerializer):
    reader = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Rentals
        fields = (
            'id',
            'reader',
            'books',
            'create_date',
            'return_date',
        )

