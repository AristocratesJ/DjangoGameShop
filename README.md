# APG Shop

APGShop is a web application built with Django that provides an online platform for users to browse, purchase, and sell video games. This project is made for web application programming course at Faculty of Mathematics and Information Science at Warsaw University of Technology.

## Features
- User Authentication - Log in, Sign in with simulated email verification (link appears in terminal)
- Forgot password function also with simulated link verification
- Store page
- Cart logic
- Adding your games to store

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/AristocratesJ/DjangoGameShop.git
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

7. Open the app in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## Technologies Used
- Django (Python)
- SQLite
- HTML, CSS

