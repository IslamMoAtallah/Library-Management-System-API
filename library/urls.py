from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LibraryUserCreateSerializer, TransactionSerializer,LibraryUserViewSet, TransactionViewSet
# Create router and register viewsets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'users', LibraryUserViewSet, basename='libraryuser')
router.register(r'transactions', TransactionViewSet, basename='transaction')
urlpatterns= [
    path('', include(router.urls)),
]