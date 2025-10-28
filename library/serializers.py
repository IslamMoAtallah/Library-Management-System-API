from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book,  LibraryUser, Transaction
class UserSerializer(serializers.ModelSerializer):
    class meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']
class LibraryUserSerializer(serializers.ModelSerializer):
    """
    Serializer for LibraryUser with related User information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = LibraryUser
        fields = [
            'id', 
            'username', 
            'email', 
            'date_of_membership', 
            'is_active', 
            'currently_borrowed_books'
        ]
        read_only_fields = ['id', 'currently_borrowed_books']
class LibraryUserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user with library profile.
    """
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True, 
        style={'input_type': 'password'},
        min_length=8
    )
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = LibraryUser
        fields = [
            'username', 
            'email', 
            'password', 
            'first_name', 
            'last_name', 
            'date_of_membership', 
            'is_active'
        ]
    def validate_username(self, value):
        """Check if username already exists."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    def validate_email(self, value):
        """Check if email already exists."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    def create(self, validated_data):
        """Create User and LibraryUser in one transaction."""
        # Extract user-related fields
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create LibraryUser profile
        library_user = LibraryUser.objects.create(user=user, **validated_data)
        return library_user
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with computed available_copies.
    """
    available_copies = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'author', 
            'isbn', 
            'published_date', 
            'number_of_copies', 
            'available_copies', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_isbn(self, value):
        """Ensure ISBN is unique for create operations."""
        if self.instance is None:  # Create operation
            if Book.objects.filter(isbn=value).exists():
                raise serializers.ValidationError("A book with this ISBN already exists.")
        return value
class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction with related object details.
    """
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    username = serializers.CharField(source='user.user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 
            'book', 
            'book_title',
            'book_author',
            'user', 
            'username', 
            'checkout_date', 
            'return_date'
        ]
        read_only_fields = ['id', 'checkout_date']
class CheckoutSerializer(serializers.Serializer):
    """
    Serializer for book checkout action.
    """
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        """Validate that book exists and has available copies."""
        try:
            book = Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")
        
        if book.available_copies <= 0:
            raise serializers.ValidationError(
                f"No copies available. All {book.number_of_copies} copies are checked out."
            )
        
        return value
class ReturnSerializer(serializers.Serializer):
    """
    Serializer for book return action.
    """
    transaction_id = serializers.IntegerField()

    def validate_transaction_id(self, value):
        """Validate that transaction exists and is not already returned."""
        try:
            transaction = Transaction.objects.get(id=value)
        except Transaction.DoesNotExist:
            raise serializers.ValidationError("Transaction not found.")
        
        if transaction.return_date is not None:
            raise serializers.ValidationError(
                "This book has already been returned."
            )
        
        return value
