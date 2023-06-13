from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from book.models import Book, Genre, Author
from rentals.models import Rentals
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.permissions import (
    AdminOnly,
    AdminOrReadOnly,
    AdminOrOwner,
    MyUserPermissions
)
from api.serializers import (
    UserSerializer,
    SignUpSerializer,
    TokenSerializer,
    RentalsSerializer,
    GenreSerializer,
    AuthorSerializer,
    BooksSerializer,
)

from api.utils import search_date_return_book

User = get_user_model()


class BooksViewSet(viewsets.ModelViewSet):
    search_fields = ('title',)
    serializer_class = BooksSerializer
    permission_classes = (AdminOrReadOnly,)
    queryset = Book.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data.get('remains'):
            request.data['remains'] += instance.remains
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('last_name',)
    queryset = Author.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('title',)
    queryset = Genre.objects.all()


class RentalsViewSet(viewsets.ModelViewSet):
    serializer_class = RentalsSerializer
    permission_classes = [IsAuthenticated, AdminOrOwner]
    queryset = Rentals.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(reader=user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        books = Book.objects.filter(pk__in=request.data.get('books'))
        for book in books:
            if book.remains == 0:
                date_return = search_date_return_book(book.id)
                return Response(
                    data=(
                        f'Книга "{book}" в данный момент отсутствует. '
                        f'Ближайшая дата поступления: '
                        f'{date_return.return_date.date().strftime("%d.%m.%Y")}'
                    ),
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
    permission_classes = (MyUserPermissions,)
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
