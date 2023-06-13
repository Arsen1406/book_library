from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from api.serializers import BooksSerializer
from book.models import Book, Genre, Author
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.permissions import AdminOnly, AdminOrReadOnly, \
    AdminOrOwner
from api.serializers import (
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
    RentalsSerializer,
    GenreSerializer,
    AuthorSerializer,
)
from rentals.models import Rentals

User = get_user_model()


class BooksViewSet(viewsets.ModelViewSet):
    search_fields = ('title',)
    serializer_class = BooksSerializer
    permission_classes = (AdminOrReadOnly,)
    queryset = Book.objects.all()


class AuthorViewSet(viewsets.ModelViewSet):
    search_fields = ('last_name',)
    serializer_class = AuthorSerializer
    permission_classes = (AdminOrReadOnly,)
    queryset = Author.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('title',)
    queryset = Genre.objects.all()


class RentalsViewSet(viewsets.ModelViewSet):
    serializer_class = RentalsSerializer
    permission_classes = (AdminOrOwner,)
    queryset = Rentals.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        books = Book.objects.filter(pk__in=request.data.get('books'))
        for book in books:
            if book.remains == 0:
                date = Rentals.objects.filter(books_pk__in)
                return Response(
                    data=(
                        f'Книга {book} в данный момнт отсутствует'
                        f'Ближайшая дата поступления'),
                    status=status.HTTP_200_OK
                )
            book.remains -= 1
            book.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    search_fields = ('username',)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user
        if self.request.method == 'PATCH':
            return self.update(request, partial=True, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


class TokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = User
    lookup_field = 'username'
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        token = str(RefreshToken.for_user(user).access_token)
        return Response(data={'token': token}, status=status.HTTP_200_OK)
