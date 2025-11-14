# alx-backend-python

## Messaging App

A Django REST Framework-based messaging application that provides a complete conversation and messaging system with user management, authentication, and RESTful API endpoints.

### 🚀 Features

- **User Management**: Custom user model with role-based permissions (Guest, Host, Admin)

- **Conversation System**: Support for both 1:1 and group conversations

- **Real-time Messaging**: Send and receive messages within conversations

- **RESTful API**: Complete CRUD operations for all entities

- **Authentication**: Session-based authentication with Django REST Framework

- **Admin Interface**: Full Django admin integration for data management

- **Nested Routing**: Clean API structure with nested conversation-messages endpoints

### 🛠️ Tech Stack

- **Backend**: Django 4.2 + Django REST Framework

- **Database**: SQLite (Development) / PostgreSQL (Production-ready)

- **Authentication**: Django REST Framework Session Authentication

- **API Documentation**: Auto-generated DRF browsable API

- **Dependencies**:

    - django-rest-framework

    - django-filter

    - drf-nested-routers

    - django-environ

### 📋 Prerequisites

- Python 3.8+

- pip (Python package manager)

### 🚀 Installation

1. Clone the repository

```bash
git clone <repository-url>
cd messaging_app
```

2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser

```bash
python manage.py createsuperuser
```

6. Run development server

```bash
python manage.py runserver
```

### 📚 API Endpoints

#### Authentication

- `GET/POST /api-auth/login/` - User login

- `GET /api-auth/logout/` - User logout

#### Users

- `GET /api/users/` - List all users

- `GET /api/users/{user_id}/` - Get user details

- `GET /api/users/me/` - Get current user details

#### Conversations

- `GET /api/conversations/` - List user's conversations

- `POST /api/conversations/` - Create new conversation

- `GET /api/conversations/{conversation_id}/` - Get conversation details

- `PUT/PATCH /api/conversations/{conversation_id}/` - Update conversation

- `DELETE /api/conversations/{conversation_id}/` - Delete conversation

### Messages

- `GET /api/messages/` - List all messages

- `POST /api/messages/` - Create new message

- `GET /api/messages/{message_id}/` - Get message details

- `GET /api/conversations/{conversation_id}/messages/` - List conversation messages

- `POST /api/conversations/{conversation_id}/messages/` - Create message in conversation

### 🗄️ Database Models

**User**

- `user_id` (UUID, Primary Key)

- `email` (Unique, Required)

- `first_name` (Required)

- `last_name` (Required)

- `password` (Required)

- `phone_number` (Optional)

- `role` (Enum: guest, host, admin)

- `created_at` (Auto-timestamp)

**Conversation**

- `conversation_id` (UUID, Primary Key)

- `created_at` (Auto-timestamp)

**ConversationParticipant**

- Junction table for many-to-many relationship between User and Conversation

**Message**

- `message_id` (UUID, Primary Key)

- `sender` (Foreign Key to User)

- `conversation` (Foreign Key to Conversation)

- `message_body` (Text, Required)

- `sent_at` (Auto-timestamp)

### 🔧 Configuration

#### Environment Variables

Create a .env file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```
#### Django Settings Key Configurations

- Custom User Model: `AUTH_USER_MODEL = 'chats.User'`

- REST Framework authentication and permissions

- CORS settings (if needed for frontend integration)

### 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

---

### 📁 Project Structure

```pgsql
messaging_app/
├── manage.py
├── requirements.txt
├── messaging_app/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── chats/                  # Main application
    ├── models.py           # Database models
    ├── serializers.py      # DRF serializers
    ├── views.py            # API viewsets
    ├── urls.py             # App URL routes
    ├── admin.py            # Admin configuration
    └── migrations/         # Database migrations
```

### 👥 User Roles

- **Guest**: Basic user permissions, can send/receive messages

- **Host**: Extended permissions for property management

- **Admin**: Full system access and user management

### 🔒 Security Features

- Password hashing and validation

- Session-based authentication

- Permission classes for API endpoints

- CORS configuration

- SQL injection protection via Django ORM

### 🚀 Deployment

For production deployment:

1. Set DEBUG = False

2. Configure proper database (PostgreSQL recommended)

3. Set up static files serving

4. Configure allowed hosts

5. Set up proper SSL/TLS certificates

### 🤝 Contributing

1. Fork the repository

2. Create a feature branch

3. Commit your changes

4. Push to the branch

5. Create a Pull Request

### 📄 License

This project is licensed under the MIT License.

### 🆘 Support

For support and questions:

- Check the API documentation at /api/ when server is running

- Review Django REST Framework documentation

- Check project issues for known problems

---

**Development Server**: http://127.0.0.1:8000/

**Admin Interface**: http://127.0.0.1:8000/admin/

**API Documentation**: Available via DRF browsable API at all endpoint URLs