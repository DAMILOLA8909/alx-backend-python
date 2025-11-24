# Django Middleware Collection

A comprehensive Django project demonstrating various custom middleware implementations for user management, security, and monitoring in a messaging application.

## 🚀 Project Overview

This project implements multiple custom Django middlewares that provide:
- **Request logging** for user activity monitoring
- **Time-based access restrictions** for maintenance windows
- **Rate limiting** to prevent spam and abuse
- **Role-based permissions** for administrative actions

## 📁 Project Structure

```pgsql
Django-Middleware-0x03/
├── chats/
│ ├── middleware.py # Custom middleware implementations
│ ├── init.py
│ └── ... (other app files)
├── messaging_app/
│ ├── settings.py # Django settings with middleware configuration
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── venv/ # Virtual environment
├── requests.log # Auto-generated request logs
├── db.sqlite3 # SQLite database
├── manage.py
├── requirements.txt
└── README.md
```

---


## 🛠️ Middleware Implementations

### 1. RequestLoggingMiddleware
**Purpose**: Logs all user requests for monitoring and debugging.

**Features**:
- Logs timestamp, username, and request path
- Handles both authenticated and anonymous users
- Writes to `requests.log` file with error fallback

**Log Format**:

2024-01-15 10:30:45.123456 - User: `admin - Path: /admin/`

2024-01-15 10:30:46.789012 - User: `Anonymous - Path: /api/messages/`

---


### 2. RestrictAccessByTimeMiddleware
**Purpose**: Enforces maintenance windows by restricting access during specific hours.

**Features**:
- Blocks access between 9:00 PM and 6:00 AM
- Returns HTTP 403 Forbidden during restricted hours
- Customizable time windows

### 3. OffensiveLanguageMiddleware (Rate Limiting)
**Purpose**: Prevents spam and abuse by limiting message frequency.

**Features**:
- IP-based rate limiting (5 messages per minute)
- Sliding time window implementation
- Thread-safe request tracking
- Returns HTTP 403 when limit exceeded

### 4. RolepermissionMiddleware
**Purpose**: Enforces role-based access control for sensitive operations.

**Features**:
- Protects specific paths requiring admin/moderator roles
- Multiple role verification methods:
  - Django's built-in `is_staff` and `is_superuser`
  - Custom user groups
  - User profile roles
- Returns HTTP 403 for unauthorized access

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Django 4.0+
- Virtualenv

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/alx-backend-python.git
   cd alx-backend-python/Django-Middleware-0x03
   ```

2. **Set up virtual environment**
```bash
   python -m venv venv

# Windows (Git Bash/MINGW64)
source venv/Scripts/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install django
# or if you have requirements.txt
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Create superuser (optional)**

```bash
python manage.py createsuperuser
```

6. **Run development server**

```bash
python manage.py runserver
```

---

### 🔧 Configuration

#### Middleware Order in settings.py

```python
MIDDLEWARE = [
    # Django built-in middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Custom middlewares
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'chats.middleware.RolepermissionMiddleware',
]
```

 #### Customization Options
 
**RequestLoggingMiddleware**

- Modify `log_file` path in middleware initialization

**RestrictAccessByTimeMiddleware**

- Change restricted hours by modifying `start_restriction` and `end_restriction`

**OffensiveLanguageMiddleware**

- Adjust rate limits: `self.limit = 5` (messages) and `self.window = 60` (seconds)

**RolepermissionMiddleware**

- Add protected paths to `self.protected_paths` list

- Extend role checking logic in `has_permission()` method

---

### 🧪 Testing

#### Manual Testing

1. Request Logging: Visit any page and check requests.log

2. Time Restrictions: Test during restricted hours (9 PM - 6 AM)

3. Rate Limiting: Send multiple POST requests within one minute

4. Role Permissions: Access protected paths with different user roles

#### Automated Testing

```bash
# Run Django test suite
python manage.py test

# Check for any configuration issues
python manage.py check
```

---

### 📊 Monitoring

#### Log Files

- requests.log: Contains all user request data

- Location: Project root directory

- Format: Timestamp - User - Path

#### Admin Interface

**Access `/admin/` to:**

- Monitor user activity

- Manage user roles and permissions

- View application metrics

---

### 🛡️ Security Features

- IP-based rate limiting prevents brute force attacks

- Time-based restrictions enable maintenance windows

- Role-based access control protects sensitive operations

- Request logging provides audit trails

---

### 🔄 API Endpoints

The project includes example endpoints for testing middleware:

`GET /` - Public access

`POST /api/messages/` - Rate-limited messaging

`GET /admin/` - Admin-only access

`POST /api/delete/` - Moderator+ required

### 🤝 Contributing

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add amazing feature`')

4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request

### 📝 License
This project is part of the ALX Backend Python curriculum.

---

### 🆘 Troubleshooting

**Common Issues**

1. Middleware not loading

    - Check middleware order in `settings.py`

    - Verify import paths are correct

2. Permission errors

    - Ensure user authentication is working

    - Check role assignments in admin interface

3. Rate limiting too aggressive

    - Adjust `self.limit` and `self.window` in `OffensiveLanguageMiddleware`

**Getting Help**

- Check Django documentation for middleware concepts

- Review middleware order in Django docs

- Examine generated log files for debugging

### 📞 Contact
For questions about this project, contact the ALX Backend Python program.
