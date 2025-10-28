from rest_framework import viewsets, status
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book, LibraryUser, Transaction 
from . serializers import (
    BookSerializer, 
    LibraryUserSerializer, 
    LibraryUserCreateSerializer,
    TransactionSerializer, 
    CheckoutSerializer, 
    ReturnSerializer
    )

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model.
    Provides CRUD operations and search/filter functionality.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
        Allow public access for list and retrieve, require auth for modifications.
        """
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Filter queryset based on query parameters.
        Supports: title, author, isbn, available
        """
        queryset = Book.objects.all()
        
        # Get query parameters
        title = self.request.query_params.get('title', None)
        author = self.request.query_params.get('author', None)
        isbn = self.request.query_params.get('isbn', None)
        available_only = self.request.query_params.get('available', None)

        # Apply filters
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn__icontains=isbn)
        
        # Filter by availability
        if available_only and available_only.lower() == 'true':
            # Filter books with available copies
            available_books = []
            for book in queryset:
                if book.available_copies > 0:
                    available_books.append(book.id)
            queryset = queryset.filter(id__in=available_books)

        return queryset


class LibraryUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for LibraryUser model.
    Handles user registration and profile management.
    """
    queryset = LibraryUser.objects.all()

    def get_serializer_class(self):
        """Use different serializer for create action."""
        if self.action == 'create':
            return LibraryUserCreateSerializer
        return LibraryUserSerializer

    def get_permissions(self):
        """Allow public access for registration, require auth for everything else."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current authenticated user's library profile.
        Endpoint: GET /api/users/me/
        """
        try:
            library_user = LibraryUser.objects.get(user=request.user)
            serializer = self.get_serializer(library_user)
            return Response(serializer.data)
        except LibraryUser.DoesNotExist:
            return Response(
                {"detail": "Library profile not found. Please create a library account."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def borrowing_history(self, request):
        """
        Get current user's complete borrowing history.
        Endpoint: GET /api/users/borrowing_history/
        """
        try:
            library_user = LibraryUser.objects.get(user=request.user)
            transactions = Transaction.objects.filter(user=library_user)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        except LibraryUser.DoesNotExist:
            return Response(
                {"detail": "Library profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Transaction model.
    Read-only for listing, with custom actions for checkout and return.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own transactions."""
        try:
            library_user = LibraryUser.objects.get(user=self.request.user)
            return Transaction.objects.filter(user=library_user)
        except LibraryUser.DoesNotExist:
            return Transaction.objects.none()

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkout(self, request):
        """
        Checkout a book.
        Endpoint: POST /api/transactions/checkout/
        Body: {"book_id": 1}
        """
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book_id = serializer.validated_data['book_id']
        book = Book.objects.get(id=book_id)

        # Get or create library user profile
        try:
            library_user = LibraryUser.objects.get(user=request.user)
        except LibraryUser.DoesNotExist:
            return Response(
                {"detail": "Library profile not found. Please create a library account first."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user account is active
        if not library_user.is_active:
            return Response(
                {"detail": "Your library account is inactive. Please contact the administrator."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if user already has this book checked out
        existing_checkout = Transaction.objects.filter(
            user=library_user,
            book=book,
            return_date__isnull=True
        ).exists()

        if existing_checkout:
            return Response(
                {"detail": "You already have this book checked out."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create transaction
        transaction = Transaction.objects.create(
            book=book,
            user=library_user
        )

        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def return_book(self, request):
        """
        Return a checked-out book.
        Endpoint: POST /api/transactions/return_book/
        Body: {"transaction_id": 1}
        """
        serializer = ReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_id = serializer.validated_data['transaction_id']
        transaction = Transaction.objects.get(id=transaction_id)

        # Verify the transaction belongs to the current user
        try:
            library_user = LibraryUser.objects.get(user=request.user)
        except LibraryUser.DoesNotExist:
            return Response(
                {"detail": "Library profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if transaction.user != library_user:
            return Response(
                {"detail": "This transaction does not belong to you."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Mark as returned
        transaction.return_date = timezone.now()
        transaction.save()

        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_200_OK
        )


# Create your views here.
