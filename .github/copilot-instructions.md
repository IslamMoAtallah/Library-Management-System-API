# Library Management System API - AI Assistant Instructions

## Project Overview
This is a Django REST API for a library management system built with Django 5.2.7 and Django REST Framework. The project follows a simple but structured architecture for managing library books.

## Core Architecture

### Project Structure
- `library_management_system_api/`: Main project configuration
  - `settings.py`: Django settings, database config (SQLite3)
  - `urls.py`: Root URL configuration
- `books/`: Main application module
  - `models.py`: Data models
  - `views.py`: API views using DRF generics
  - `serializers.py`: DRF serializers
  - `urls.py`: App-level URL routing

### Key Patterns
1. **REST API Design**:
   - Uses Django REST Framework's generic views (`generics.ListCreateAPIView`)
   - API endpoints follow RESTful conventions (see `books/urls.py`)
   - Serializers use ModelSerializer for automatic field mapping

2. **Data Model Structure**:
   ```python
   # Example from books/models.py
   class Book(models.Model):
       title = models.CharField(max_length=200)
       author = models.CharField(max_length=200)
       published_date = models.DateField()
   ```

## Development Workflow

### Setup
1. Ensure Python and Django are installed
2. Create and activate virtual environment
3. Install dependencies: `pip install django djangorestframework`
4. Run migrations: `python manage.py migrate`
5. Start development server: `python manage.py runserver`

### Testing
- Use Django's test framework
- Test files are organized in each app's `tests.py`

### API Endpoints
- `POST /books`: Create new book
- `GET /books`: List all books

## Common Tasks
1. **Adding New Models**:
   - Create model in `books/models.py`
   - Create serializer in `books/serializers.py`
   - Add view in `books/views.py`
   - Register URL in `books/urls.py`

2. **Database Changes**:
   - Make model changes
   - Create migrations: `python manage.py makemigrations`
   - Apply migrations: `python manage.py migrate`

## Project-Specific Conventions
1. Model naming follows singular form (e.g., `Book` not `Books`)
2. API views use DRF generic views when possible
3. URLs are lowercase, no trailing slashes
4. All model fields use explicit max_lengths for CharField