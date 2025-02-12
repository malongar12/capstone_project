# Library Management System

## Overview

The **Library Management System** is a web application built with **Python** and **Flask**. The app allows users to sign up, log in, browse, borrow, and return books, while administrators can manage users and books. The system integrates with the **Google Books API** for fetching book details and enables efficient management through a user-friendly interface.

### Key Features:
- **User Management**: Users can sign up, log in, and manage their accounts.
- **Admin Management**: Admin users have extra privileges to manage books and users.
- **Book Management**: Books can be added, deleted, and checked out by users.
- **Checkouts**: Users can borrow books up to 3 at a time.
- **Admin Dashboard**: Admins can add new books, delete books, view all users, and manage issued books.

## Technologies Used
- **Python**: Programming language for backend development.
- **Flask**: Web framework for creating the application.
- **PostgreSQL**: Relational database management system used to store user and book data.
- **SQLAlchemy**: ORM (Object Relational Mapping) tool for interacting with the database.
- **Jinja**: Template engine for rendering dynamic HTML content.
- **CSS**: Styling language for creating responsive and visually appealing web pages.
- **Flask-Bcrypt**: Used to securely hash passwords.
- **Google Books API**: External API used to fetch book details.

## Installation and Setup

### Prerequisites

Ensure the following are installed on your machine:
- **Python** 3.x
- **PostgreSQL** (or another database)
- **pip** (Python package manager)

### Steps to Install and Run the Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/library-management-system.git
   cd library-management-system
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL Database**:
   - Create a new PostgreSQL database called `library_db`.
   ```bash
   createdb library_db
   ```

5. **Configure Database in `config.py`**:
   - Make sure to set your **PostgreSQL credentials** in the configuration file.
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/library_db'
   ```

6. **Run Database Migrations**:
   - Create the database tables by running the migrations.
   ```bash
   python manage.py db upgrade
   ```

7. **Set up Environment Variables**:
   - Define any required environment variables like `GOOGLE_API_KEY` for interacting with the Google Books API.

8. **Start the Application**:
   ```bash
   python app.py
   ```

   Your Flask application should now be running on `http://localhost:5000`.

## Features and Endpoints

### 1. **User Routes**:
- **`/signup`**: User signup page where users can create an account.
- **`/login`**: User login page for authentication.
- **`/logout`**: Logs the user out and redirects to the home page.
- **`/users`**: View a list of all users (Admin only).

### 2. **Admin Routes**:
- **`/admin/signup`**: Admin signup page to create a new admin account.
- **`/admin/login`**: Admin login page for admin authentication.
- **`/admin/dashboard`**: Admin dashboard for managing books and users.
- **`/admin/logout`**: Admin logout.

### 3. **Book Routes**:
- **`/books`**: View all books.
- **`/book/<int:id>`**: View a specific book's details.
- **`/book/add`**: Admin route for adding new books to the system.
- **`/book/<int:id>/delete`**: Admin route for deleting a book.
- **`/book/<int:id>/issue`**: Users can borrow a book (limited to 3 books).
- **`/book/<int:id>/return`**: Users can return a borrowed book.
- **`/book/issued/view`**: View a list of all books the user has checked out.

### 4. **API Endpoints**:
- **`/api/books`**: Get the list of all books (GET request).
- **`/api/books/<book_id>`**: Get details of a specific book (GET request).
- **`/api/books/add`**: Admin endpoint for adding a book (POST request).
- **`/api/books/delete/<book_id>`**: Admin endpoint for deleting a book (DELETE request).
- **`/api/users`**: Get the list of all users (GET request).
- **`/api/users/<user_id>`**: Get details of a specific user (GET request).

## Flash Messaging

Flash messages are used to provide feedback to users and admins. They include:
- **Success messages**: For successful operations like user registration or book addition.
- **Error messages**: For incorrect operations like invalid email, incorrect password, or failed login.

### Example of Flash Messages:
```python
flash("Book was added successfully!")
flash("Error: Admin pin must be a numeric value.", 'error')
```

## Frontend

The frontend of this application is built using **HTML**, **CSS**, and **Jinja** templating. It provides an intuitive interface with the following features:
- **User Interface**: Allows users to browse, check out, and return books.
- **Admin Interface**: A separate dashboard for admins to manage the library's users and books.

## Database Schema

The application uses **PostgreSQL** as the database to store user and book data. The key tables in the database include:
1. **Users**: Stores information like name, email, password (hashed), and admin number.
2. **Books**: Stores book details like title, author, description, and the number of copies.
3. **Copies**: Tracks the books issued to users, including the issue date and return date.

## Running Tests

You can write unit tests to test various parts of the application. Ensure your application is properly set up with mock data before running the tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

