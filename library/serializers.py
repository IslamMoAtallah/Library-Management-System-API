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
