# Flask CRUD App with Authentication

This is a beginner-friendly Flask application with user authentication and a student management CRUD system. It uses MySQL via XAMPP for data storage.

## Features

- User registration and login
- Password hashing with Werkzeug
- Session-based authentication
- CRUD operations for students
- Bootstrap frontend and Jinja2 templates
- Search students
- Flash messages for feedback

## Requirements

- Python 3.10+
- XAMPP with MySQL running
- `mysql-connector-python`
- `Flask`

## Installation

1. Open XAMPP Control Panel and start `Apache` and `MySQL`.
2. Open `phpMyAdmin` and create a new database named `flask_crud_db`.
3. Create the tables by running the SQL script below or importing `db_setup.sql`.
4. Install Python dependencies:

```bash
cd c:\Users\Test\Desktop\parvam\flask_crud_app
python -m pip install -r requirements.txt
```

## Database Setup

Run the following SQL in phpMyAdmin or in your MySQL client:

```sql
CREATE DATABASE IF NOT EXISTS flask_crud_db;
USE flask_crud_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL,
  course VARCHAR(100) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  is_active BIT(1) NOT NULL DEFAULT b'1'
);
```

This app uses a MySQL `BIT(1)` column named `is_active` to store student active/inactive status.

## Configuration

The MySQL connection settings are located in `app.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flask_crud_db'
}
```

If your XAMPP MySQL user or password is different, update these values.

## Run the App

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## App Routes

- `/register` - Register new users
- `/login` - Login page
- `/dashboard` - Protected dashboard
- `/students` - View students
- `/add_student` - Add new student
- `/edit_student/<id>` - Edit student
- `/delete_student/<id>` - Delete student
- `/logout` - Logout user

## Notes

- The app uses Flask `session` to protect dashboard and student routes.
- Passwords are hashed before storing in MySQL.
- Flash messages show success or error feedback.
