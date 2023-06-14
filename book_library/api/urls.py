from django.urls import path, include
from rest_framework import routers
from api import views


router_v1 = routers.DefaultRouter()
router_v1.register(r'books', views.BooksViewSet, basename='book')
router_v1.register(r'genre', views.GenreViewSet, basename='genre')
router_v1.register(r'authors', views.AuthorViewSet, basename='authors')
router_v1.register(r'rentals', views.RentalsViewSet, basename='rentals')

router_v1.register(r'auth/signup', views.SignUpViewSet, basename='signup')
router_v1.register(r'auth/token', views.TokenViewSet, basename='token')
router_v1.register(r'users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]