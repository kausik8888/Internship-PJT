# Internship-PJT
FullstackDevlop in WebPage
Signup and Login Page - Django Application
This project is a Django-based web application that implements a user signup and login system. PostgreSQL is used as the database, and the frontend is built using HTML and CSS for styling.

Features
User Signup: Allows new users to create an account.
User Login: Registered users can log in using their credentials.
User Authentication: Protects pages that require authentication, and provides logout functionality.
Database: PostgreSQL is used for storing user information.
Frontend: Simple user interface using HTML for structure and CSS for styling.
Technologies Used
Backend: Django (Python web framework)
Frontend: HTML, CSS
Database: PostgreSQL
Others: Django ORM for database handling
Prerequisites
Make sure you have the following installed:

Python 3.x
Django (version 4.x or above recommended)
PostgreSQL
Pip (Python package installer)
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/django-signup-login.git
cd django-signup-login
2. Install Dependencies
Create a virtual environment and install the required Python packages:

bash
Copy code
# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate    # On Linux/MacOS
# or
env\Scripts\activate       # On Windows

# Install dependencies
pip install -r requirements.txt
3. Setup PostgreSQL Database
Install PostgreSQL if you haven't already.
Create a new database and user for this project:
sql
Copy code
CREATE DATABASE yourdbname;
CREATE USER yourusername WITH PASSWORD 'yourpassword';
ALTER ROLE yourusername SET client_encoding TO 'utf8';
ALTER ROLE yourusername SET default_transaction_isolation TO 'read committed';
ALTER ROLE yourusername SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE yourdbname TO yourusername;
Update the database configuration in settings.py:
python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourusername',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
4. Apply Migrations
Run Django migrations to create the required database tables:

bash
Copy code
python manage.py migrate
5. Create a Superuser (Admin)
Create an admin user to access the Django admin panel:

bash
Copy code
python manage.py createsuperuser
6. Run the Development Server
Start the Django development server:

bash
Copy code
python manage.py runserver
Visit http://127.0.0.1:8000 to view the application.

File Structure
bash
Copy code
django-signup-login/
│
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│
├── users/  # Django app for user management
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/  # Contains login.html, signup.html
│   ├── views.py
│   ├── forms.py  # Custom forms for signup
│   ├── urls.py   # URLs for signup, login
│   ├── models.py
│
├── static/  # Contains CSS files for styling
│   ├── styles.css
│
├── db.sqlite3
├── manage.py
└── README.md
Key Files
settings.py: Django project settings, including database configuration.
urls.py: Project-level URLs, includes routing for the login and signup views.
views.py: Contains logic for user signup, login, and authentication.
forms.py: Defines Django forms for user registration.
templates/registration/: HTML files for signup and login forms.
static/: CSS files for styling.
Running Tests
To run tests for the application:

bash
Copy code
python manage.py test
Deployment
Setup environment variables for production.
Use services like Heroku or deploy on a cloud platform that supports Django and PostgreSQL.
