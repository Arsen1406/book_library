from django.urls import path, include
from rest_framework import routers
from api.views import BooksViewSet

from api.views import (
    SignUpViewSet,
    TokenViewSet,
    UsersViewSet,
    GenreViewSet,
    AuthorViewSet,
    RentalsViewSet,
)


router_v1 = routers.DefaultRouter()
router_v1.register(r'books', BooksViewSet, basename='book')
router_v1.register(r'genre', GenreViewSet, basename='genre')
router_v1.register(r'authors', AuthorViewSet, basename='authors')
router_v1.register(r'rentals', RentalsViewSet, basename='rentals')

router_v1.register(r'auth/signup', SignUpViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    # path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]