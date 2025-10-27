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
    def __str__(self):
        return f"{self.title} by {self.author}"

    
