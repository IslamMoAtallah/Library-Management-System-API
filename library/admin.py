from django.contrib import admin
from .models import Book, LibraryUser, Transaction
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display= [
        'title',
        'author',
        'isbn',
        'published_date',
        "number_of_copies",

    ]
    list_filter = ['published_date', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'get_available_copies']
    def get_available_copies(self, obj):
        return obj.available_copies
    get_available_copies.short_description = 'Available Copies'

# Register your models here.
@admin.register(LibraryUser)
class LibraryUserAdmin(admin.ModelAdmin):
    list_display= [
        'user', 
        'date_of_membership', 
        'is_active', 
        'get_borrowed_books',
    ]

    list_filter = ['is_active', 'date_of_membership']
    def get_borrowed_books(self, obj):
        return obj.currently_borrowed_books
    get_borrowed_books.short_description = 'Currently Borrowed'
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user', 
        'book', 
        'checkout_date', 
        'return_date',
        'get_status',
    ]
    list_filter = ['checkout_date', 'return_date']
    def get_status(self, obj):
        return "Returned" if obj.return_date else 'Checked out'
    get_status.short_description= 'Status'
    
