from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator



# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(
        max_length=13, 
        unique=True,
        help_text="13-digit ISBN number"
    )
    published_date = models.DateField()
    number_of_copies = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text= "total number of copies in library"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title} by {self.author}"

    def available_copies(self):
        # Count the number of available books by subtracting the checked out books
        checked_out= Transaction.objects.filter(
            book =self, 
            return_date_isnull= True
        ).count()
        return self.number_of_copies - checked_out
class LibraryUser(models.Model):
    # extend user profile for library members 
    # by One-to-one relationship with Django built-in user model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='library_profile'
    )
    date_of_membership = models.DateField(auto_now_add= True)
    is_active= models.BooleanField( default= True)
    class Meta:
        verbose_name= 'library User'
    def __str__ (self):
        return f"{self.user}s Library profile"
class Transaction (models.Model):
    # Tracking book checkouts and returns
    book = models.ForeignKey(
        Book, 
        on_delete= models.CASCADE,
        related_name= 'transactions'
    ) 
    user = models.ForeignKey(
        LibraryUser,
        on_delete= models.CASCADE,
        related_name="Transactions")
    checkout_date = models.DateTimeField(auto_now_add= True)
    return_date = models.DateField(
        null= True,
        blank= True
    )
    def __str__(self):
        status= 'Returned' if self.return_date else 'Checkout'
        return f"{self.user.user} - {self.book.title} ({status})"
    