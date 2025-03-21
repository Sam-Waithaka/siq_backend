# Django User Management API

A RESTful API built with Django and Django REST Framework that provides a complete user management system with JWT authentication.

## Features

- User registration with email-based authentication
- JWT-based login with access and refresh tokens
- User profile management
- API documentation with Swagger/OpenAPI
- Comprehensive test suite

## Tech Stack

- Python 3.8+
- Django 5.1.7
- Django REST Framework 3.15.2
- PostgreSQL (database)
- Django REST Framework Simple JWT
- drf-yasg (Swagger/OpenAPI documentation)

## Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── config/                 # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Django settings, JWT configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py
├── users/          # User app
│   ├── __init__.py
│   ├── admin.py              # Admin interface configuration
│   ├── apps.py
│   ├── migrations/           # Database migrations
│   ├── models.py             # Custom user model
│   ├── serializers.py        # API serializers
│   ├── tests.py              # Test suite
│   ├── urls.py               # App URL routing
│   └── views.py              # API endpoints
```

## API Endpoints

| Endpoint | Method | Description | Authentication Required |
|----------|--------|-------------|------------------------|
| `/api/register/` | POST | Create a new user account | No |
| `/api/login/` | POST | Login and get JWT tokens | No |
| `/api/token/refresh/` | POST | Refresh access token | No |
| `/api/profile/` | GET | Get user profile details | Yes |
| `/api/profile/` | PUT/PATCH | Update user profile | Yes |
| `/swagger/` | GET | Swagger API documentation | No |
| `/redoc/` | GET | ReDoc API documentation | No |

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Sam-Waithaka/SIQ_Backend.git
   cd SIQ_Backend
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Configure the database
   - Create a PostgreSQL database named `user_management_db`
   - Update database settings in `user_api/settings.py` if needed

6. Apply database migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server
   ```bash
   python manage.py runserver
   ```

9. Access the API at http://127.0.0.1:8000/api/
   - Swagger documentation: http://127.0.0.1:8000/swagger/
   - ReDoc documentation: http://127.0.0.1:8000/redoc/

## Running Tests

Run the test suite with:
```bash
python manage.py test users
```

To run specific test classes:
```bash
python manage.py test users.tests.UserRegistrationTests
```

## Authentication

This API uses JWT (JSON Web Token) authentication. To authenticate requests:

1. Login to get access and refresh tokens
2. Add the access token to the Authorization header:
   ```
   Authorization: Bearer <access-token>
   ```
3. When the access token expires, use the refresh token to get a new access token

## Sample API Requests

### Register a New User

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "password": "SecurePassword123!", "password2": "SecurePassword123!"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "SecurePassword123!"}'
```

### Get User Profile

```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Bearer <access-token>"
```

### Update User Profile

```bash
curl -X PATCH http://127.0.0.1:8000/api/profile/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access-token>" \
  -d '{"name": "John Smith"}'
```

## Security Considerations

- Passwords are securely hashed using Django's password hashing system
- JWT tokens have short lifetimes to limit the risk of token theft
- HTTPS should be enabled in production environments
- API endpoints have appropriate permission classes

## License

[MIT License](LICENSE)
