# Library-Management-System-API
<!-- Features
Core Functionality

 Book Management: Complete CRUD operations for library books
 User Management: User registration and profile management
Checkout System: Borrow and return books with automatic inventory tracking
 Search & Filter: Find books by title, author, ISBN, or availability
 Transaction History: Complete audit trail of all checkouts and returns
Authentication: Secure JWT-based authentication system

Key Features

 Real-time book availability tracking
 Advanced search and filtering capabilities
 User borrowing history Role-based access control
 Paginated API responses
 Browsable API interface
 Optimized database queries with indexing
 Comprehensive data validation
 -->
 <!-- Backend

Python 3.13+ - Programming language
Django 5.2.7 - Web framework
Django REST Framework 3.14+ - API framework
Django REST Framework SimpleJWT - JWT authentication -->


<!-- Tools

Git - Version control
pip - Package management
virtualenv - Environment isolation -->
<!-- Database Models
Book

title, author, isbn (unique)
published_date, number_of_copies
available_copies (computed)

LibraryUser

OneToOne with Django User
date_of_membership, is_active
currently_borrowed_books (computed)

Transaction

ForeignKey to Book and LibraryUser
checkout_date, return_date

Relationships:

User (1:1) LibraryUser
LibraryUser (1:N) Transaction
Book (1:N) Transaction -->
<!--  Business Rules
Checkout

✓ Book must have available copies
✓ User account must be active
✓ User cannot checkout same book twice
✓ Available copies decrease automatically

Return

✓ Transaction must exist
✓ Must belong to authenticated user
✓ Book must not already be returned
✓ Available copies increase automatically -->
<!-- What i have buit so far 
What You've Built So Far:
1. Database Models - Book, LibraryUser, Transaction
2. Admin Interface - Full CRUD with custom displays
3. Serializers - Data validation and transformation
4. API Endpoints - 19 RESTful endpoints
5. Authentication - JWT token-based
6. Business Logic - Checkout/return with validations
7.Search & Filter - Query parameters working -->