# E-Learning Platform
A simple E-Learning platform based on the Django web framework.

## Installation
1. Clone the repository
2. Ensure you have Python 3.11 or higher installed
3. Run `python -m venv env` to create a virtual environment
4. Run `source env/bin/activate` to activate the virtual environment (Linux/MacOS) or `env\Scripts\activate` (Windows)
5. Run `python -m pip install -r requirements.txt` to install the required packages from requirements.txt
6. Create a `.env` file (as shown in the `.env.sample` file) in the root directory of the project and add the following variables as per 
your database configuration (PostgreSQL is used in this project):

    ```
        SECRET_KEY=your_secret_key
        DB_NAME=your database name
        DB_USER=your database user
        DB_PASSWORD=your database password
        DB_HOST=your database host
        DB_PORT=your database port
    ```
   Note: The `SECRET_KEY` variable is used by Django to provide cryptographic signing, and should be kept secret. 
   
   Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
   in a terminal to generate a new secret key.


7. Run `python manage.py makemigrations`
8. Run `python manage.py migrate`
9. Run `python manage.py runserver`
10. Visit `localhost:8000` in your browser

# Features
### Admin
- Create, update and delete users, courses, lessons, and quizzes
- View user progress
- View user quiz results
- Every aspect of the platform

### Teacher
- Create study materials, quizzes, and assignments
- Mark and grade assignments, quizzes, tests

### Student
- View courses, lessons, and quizzes
- Download study materials
- Take quizzes
- View quiz results
- Take assignments

### Users
- Send each other messages using django-messages

## Deployment to Azure App Service
- For production, the platform can can be deployed using Azure App Service.
- Follow guidelines on how to set up app service, a postgresql database as well as an Azure storage accounts, then pass them as environment variables.

## Using Containers (Docker)





