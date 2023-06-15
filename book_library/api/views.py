from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from book.models import Book, Genre, Author
from rentals.models import Rentals
from api import permissions, serializers

User = get_user_model()


class BooksViewSet(viewsets.ModelViewSet):
    search_fields = ('title',)
    serializer_class = serializers.BooksSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    queryset = Book.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data.get('remains'):
            request.data['remains'] += instance.remains
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    search_fields = ('last_name',)
    queryset = Author.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    search_fields = ('title',)
    queryset = Genre.objects.all()


class RentalsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RentalsSerializer
    permission_classes = [IsAuthenticated, permissions.AdminOrOwner]
    queryset = Rentals.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return serializers.RentalsSerializer
        return serializers.RentalsViewSerializer

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
                rentals = Rentals.objects.filter(
                    books__id__in=[book.id]
                ).order_by('return_date')[0]
                return Response(
                    data=(
                        f'Книга "{book}" в данный момент отсутствует. '
                        f'Ближайшая дата поступления: '
                        f'{rentals.return_date.date().strftime("%d.%m.%Y")}'
                    ),
                    status=status.HTTP_200_OK
                )
            book.views += 1
            book.remains -= 1
            book.save()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(reader=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = kwargs['pk']
        rentals = Rentals.objects.prefetch_related('books').get(id=pk)
        for book in rentals.books.all():
            book.remains += 1
            book.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AdminOnly]
    search_fields = ('username',)
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.kwargs['username'] = self.request.user
        if self.request.method == 'PATCH':
            return self.update(request, partial=True, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SignUpSerializer

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
    serializer_class = serializers.TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        password = request.data.get('password')
        if password and user.password == password:
            token = str(RefreshToken.for_user(user).access_token)
            return Response(data={'token': token}, status=status.HTTP_200_OK)
        return Response(
            data='Вы не предоставили пароль!',
            status=status.HTTP_403_FORBIDDEN
        )
