# 🏫 Fatima Convent Senior Secondary School Website

<div align="center">

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-3.x+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

A modern, feature-rich Django-based content management system (CMS) for educational institutions. Designed specifically for Fatima Convent Senior Secondary School, this application provides an intuitive platform for school administrators to manage and showcase school information, events, and multimedia content.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

---

## 📖 Overview

The Fatima Convent Senior Secondary School Website is a comprehensive web application built with Django, enabling school administrators to manage and display:

- **Dynamic Homepage** with customizable banner slideshow
- **Institutional Information** including school history, mission, and principal details
- **Media Gallery** with organized photo and video content
- **News & Updates** for communicating important announcements
- **Fee Structure** information for students and parents
- **Newsletter Subscription** system for alumni engagement
- **Admin Dashboard** for easy content management without coding

This project demonstrates best practices in Django development, including proper model design, template hierarchy, and static file management.

---

## ✨ Features

### Core Features

- ✅ **Dynamic Banner Management** - Admin-managed homepage banners with image support
- ✅ **About Section** - Dedicated page for school history, principal profile, and institutional information
- ✅ **Gallery System** - Categorized image and video gallery with media organization
- ✅ **Newsletter System** - Email subscription functionality for alumni and interested parties
- ✅ **News Updates** - Real-time updates and announcements management
- ✅ **Fee Structure** - Display and manage school fee information

### Technical Features

- ✅ **Django Admin Panel** - Comprehensive admin interface for content management
- ✅ **Responsive Design** - Mobile-friendly interface using Bootstrap 4+
- ✅ **Static Asset Management** - Optimized CSS, JavaScript, and image handling
- ✅ **Database Migrations** - Version-controlled database schema management
- ✅ **Media Upload Support** - Easy image and video uploads with Django's media handling
- ✅ **SEO-Friendly** - Structured URLs and semantic HTML templates

---

## 🛠️ Technology Stack

| Category                 | Technology                                                  |
| ------------------------ | ----------------------------------------------------------- |
| **Backend**              | Python 3.x, Django 3.x+                                     |
| **Database**             | SQLite3 (development), PostgreSQL (production)              |
| **Frontend**             | HTML5, CSS3, JavaScript (ES6+)                              |
| **CSS Framework**        | Bootstrap 4+                                                |
| **Icon Library**         | Font Awesome                                                |
| **JavaScript Libraries** | jQuery, Owl Carousel, Masonry, Magnific Popup, ScrollReveal |
| **Package Manager**      | pip                                                         |
| **Version Control**      | Git                                                         |

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/)
- **pip** - Usually comes with Python
- **Virtual Environment** - Built-in with Python (venv)

### System Requirements

- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 512MB (1GB recommended)
- **Disk Space**: Minimum 500MB
- **Browser**: Modern browser with JavaScript enabled

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/mrinmoy-hex/FCSS-WEB.git
cd FCSS-WEB
```

### Step 2: Create Virtual Environment

It's best practice to use a virtual environment to isolate project dependencies.

**Windows (PowerShell):**

```powershell
python -m venv myenv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
myenv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python -m venv myenv
myenv\Scripts\activate.bat
```

**macOS/Linux:**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs all required packages including Django, Pillow (for image handling), and other dependencies specified in `requirements.txt`.

---

## ⚙️ Configuration

### Environment Setup

1. **Database Setup:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

   These commands create the SQLite database and apply all migrations.

2. **Create Superuser Account:**

   ```bash
   python manage.py createsuperuser
   ```

   You'll be prompted to enter username, email, and password. Use a secure password for production.

3. **Collect Static Files** (for production):
   ```bash
   python manage.py collectstatic --noinput
   ```
   This gathers all static files (CSS, JS, images) into `staticfiles/` directory.

### Settings Configuration

Edit `SchoolApp/settings.py` to customize:

```python
# Key settings you may want to adjust:
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add your domain
DATABASES = {...}  # Database configuration
STATIC_URL = '/static/'  # Static files URL
MEDIA_URL = '/media/'  # Media files URL
```

---

## 📝 Usage

### Running the Development Server

Start the development server with:

```bash
python manage.py runserver
```

The application will be available at:

- **Frontend:** `http://127.0.0.1:8000/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

### Accessing the Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Manage content for:
   - **Banners** - Homepage banner images and text
   - **About Section** - School information and principal details
   - **Gallery** - Photos and videos organized by category
   - **Newsletter Subscribers** - Manage email subscriptions
   - **News Updates** - Create and publish announcements
   - **Fee Structure** - Maintain fee information

---

## 📁 Project Structure

```
FCSS-WEB/
├── App/                          # Main Django application
│   ├── migrations/               # Database migration files
│   ├── models.py                 # Database models definition
│   ├── views.py                  # View logic for rendering pages
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Django admin configuration
│   └── tests.py                  # Unit tests
│
├── SchoolApp/                    # Django project configuration
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Project-level URL routing
│   ├── wsgi.py                   # WSGI application for deployment
│   └── asgi.py                   # ASGI application for async support
│
├── templates/                    # HTML templates
│   ├── base.html                 # Base template (inherited by all pages)
│   ├── index.html                # Homepage
│   ├── about.html                # About page
│   ├── gallery.html              # Gallery page
│   ├── contact.html              # Contact page
│   ├── fee_structure.html        # Fee structure page
│   └── admin/                    # Admin templates
│
├── static/                       # Static assets (CSS, JS, images)
│   ├── css/                      # Stylesheets
│   ├── js/                       # JavaScript files
│   ├── images/                   # Image assets
│   └── vendors/                  # Third-party libraries
│
├── media/                        # User-uploaded content
│   ├── banner_images/
│   ├── about_images/
│   └── gallery_images/
│
├── myenv/                        # Virtual environment directory
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── db.sqlite3                    # SQLite database
├── Procfile                      # Deployment configuration
└── README.md                     # This file
```

---

## 💾 Database Models

### Core Models

#### 1. **Banner**

Represents homepage banner content with images and text.

```python
- title: String
- image: Image field
- description: Text
- created_at: DateTime
- updated_at: DateTime
```

#### 2. **About**

Stores school information, history, and principal details.

```python
- title: String
- principal_name: String
- principal_image: Image field
- school_story: Text
- description: Text
- created_at: DateTime
- updated_at: DateTime
```

#### 3. **GalleryItem**

Manages gallery photos and videos with categorization.

```python
- category: String (choices-based)
- photo: Image field
- video: URL/Video field
- caption: String
- created_at: DateTime
- updated_at: DateTime
```

#### 4. **NewsletterSubscriber**

Maintains email subscription list.

```python
- email: Email field (unique)
- subscribed_at: DateTime
- is_active: Boolean
```

#### 5. **NewsUpdate**

Handles news and announcements.

```python
- title: String
- content: Text
- published_date: DateTime
- is_published: Boolean
```

#### 6. **FeeStructure**

Displays school fee information.

```python
- class: String
- annual_fee: Decimal
- monthly_fee: Decimal
- description: Text
```

---

## 🔗 API Endpoints

| HTTP Method | Endpoint          | Description                         |
| ----------- | ----------------- | ----------------------------------- |
| GET         | `/`               | Homepage with banner slideshow      |
| GET         | `/about/`         | About page with school information  |
| GET         | `/gallery/`       | Gallery page with categorized media |
| GET         | `/contact/`       | Contact page                        |
| GET         | `/fee_structure/` | Fee structure information           |
| GET         | `/admin/`         | Admin dashboard                     |

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Virtual Environment Not Activating**

**Problem:** `Cannot find myenv\Scripts\Activate.ps1`

**Solution:**

```bash
# Ensure you're in the project root directory
cd FCSS-WEB

# Recreate virtual environment
python -m venv myenv
```

#### 2. **Module Import Errors**

**Problem:** `ModuleNotFoundError: No module named 'django'`

**Solution:**

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

#### 3. **Database Migration Errors**

**Problem:** `django.db.utils.OperationalError`

**Solution:**

```bash
# Reset migrations (development only!)
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

#### 4. **Static Files Not Loading**

**Problem:** CSS/JS not displaying in browser

**Solution:**

```bash
# Collect static files
python manage.py collectstatic --clear --noinput

# Ensure DEBUG = True in development
# Check STATIC_URL and STATIC_ROOT in settings.py
```

#### 5. **Port 8000 Already in Use**

**Problem:** `Address already in use`

**Solution:**

```bash
# Use a different port
python manage.py runserver 8001

# Or kill the process using port 8000
```

#### 6. **Permission Denied on Activation Script** (PowerShell)

**Problem:** `cannot be loaded because running scripts is disabled`

**Solution:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

---

## 🚢 Deployment

### Production Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use environment variables for sensitive data (database credentials, secret keys)
- [ ] Set up PostgreSQL database for production
- [ ] Configure static file serving (CDN or web server)
- [ ] Set up media file handling
- [ ] Enable HTTPS
- [ ] Configure email backend for newsletter functionality
- [ ] Set up regular database backups
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Configure web server (Nginx, Apache)

### Deployment Platforms

This application can be deployed on:

- **Heroku** - See `Procfile` for configuration
- **PythonAnywhere**
- **DigitalOcean**
- **AWS EC2**
- **Azure App Service**
- **Self-hosted VPS**

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork the Repository**

   ```bash
   # Click "Fork" on GitHub to create your own copy
   ```

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your-username/FCSS-WEB.git
   cd FCSS-WEB
   ```

3. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```

4. **Make Your Changes**
   - Follow Django best practices
   - Write clean, readable code
   - Add comments for complex logic
   - Update relevant documentation

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: Brief description of changes"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes in detail
   - Reference any related issues

### Contribution Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use meaningful variable and function names
- Include docstrings for classes and functions
- Write unit tests for new features
- Update README.md if adding new features
- Keep commits atomic and well-documented

### Code Style

```python
# Good example
def get_gallery_items(category=None):
    """
    Retrieve gallery items, optionally filtered by category.

    Args:
        category (str, optional): Filter by category name

    Returns:
        QuerySet: Filtered gallery items
    """
    queryset = GalleryItem.objects.all()
    if category:
        queryset = queryset.filter(category=category)
    return queryset
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What You Can Do

- ✅ Use for commercial and private purposes
- ✅ Modify the code
- ✅ Distribute the software
- ✅ Use it with restrictions

### Conditions

- Include the original copyright notice and license
- Provide a copy of the license

---

## 📞 Support

### Getting Help

- **Documentation:** See [Project Structure](#project-structure) and [Database Models](#database-models)
- **Issues:** [GitHub Issues](https://github.com/mrinmoy-hex/FCSS-WEB/issues)
- **Discussions:** [GitHub Discussions](https://github.com/mrinmoy-hex/FCSS-WEB/discussions)

### Reporting Bugs

When reporting a bug, please include:

1. Python version
2. Django version
3. Steps to reproduce
4. Expected behavior
5. Actual behavior
6. Error traceback (if applicable)
7. Screenshots (if applicable)

### Feature Requests

To suggest a new feature:

1. Check if it's already been requested in [Issues](https://github.com/mrinmoy-hex/FCSS-WEB/issues)
2. Create a new issue with the title "Feature Request: [Description]"
3. Describe the feature and why it would be useful

---

## 📚 Additional Resources

### Django Documentation

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)

### Frontend Frameworks

- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [jQuery Documentation](https://api.jquery.com/)
- [Font Awesome Icons](https://fontawesome.com/icons)

### Best Practices

- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Real Python - Django](https://realpython.com/tutorials/django/)
- [Django Design Patterns](https://www.django-rest-framework.org/)

---

## 🎯 Roadmap

Planned features and improvements:

- [ ] Student management system
- [ ] Online admission portal
- [ ] Class scheduling and timetable
- [ ] Assignment and homework submission
- [ ] Parent-teacher communication system
- [ ] Mobile application
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Search functionality
- [ ] Multi-language support
- [ ] Analytics and reporting dashboard

---

## 👨‍💻 Authors & Contributors

**Original Author:** [Mrinmoy](https://github.com/mrinmoy-hex) and [WIZARDOF-OZ](https://github.com/WIZARDOF-OZ)

### Contributors

- [Your Name](https://github.com/yourprofile) - Contributions

---

## 🙏 Acknowledgments

- Django community for excellent framework and documentation
- Bootstrap team for responsive CSS framework
- Font Awesome for icon library
- All contributors and supporters of this project

---

<div align="center">

**Built with ❤️ for Fatima Convent Senior Secondary School**

[⬆ back to top](#-fatima-convent-senior-secondary-school-website)

</div>
