from django.urls import path, include
from rest_framework import routers
from api.views import BooksViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'books', BooksViewSet, basename='books')

# router_v1.register(r'auth/signup', SignUpViewSet, basename='signup')
# router_v1.register(r'auth/token', TokenViewSet, basename='token')
# router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]