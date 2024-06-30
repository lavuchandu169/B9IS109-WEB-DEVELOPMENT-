# B9IS109-WEB-DEVELOPMENT-
# To-Do List Web Application

A simple To-Do List application built using Flask, SQLAlchemy, and JWT for authentication.

## Features

- User registration and login
- JWT-based authentication
- Task management (add, view, delete tasks)
- Role-based user permissions

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Flask-Bcrypt
- JWT
- HTML/CSS
- JavaScript (Fetch API)

## Requirements

- Python 3.7+
- Virtual Environment

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/lavuchandu169/to-do-list-app.git
    cd to-do-list-app
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```sh
    flask run
    ```

5. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:5000/
    ```

## Usage

### Register a New User

1. Navigate to the registration page from the home page.
2. Fill in the username and password fields.
3. Submit the form to create a new account.

### Login

1. Navigate to the login page from the home page.
2. Fill in your username and password.
3. Submit the form to log in.

### Manage Tasks

- **Add Task**: Enter a new task in the input field and click "Add Task".
- **View Tasks**: All tasks are displayed in a list.
- **Delete Task**: Click the "Delete" button next to a task to remove it.

## Project Structure

to-do-list-app/
│
├── app.py
├── requirements.txt
├── templates/
│ ├── home.html
│ ├── login.html
│ ├── register.html
│ └── index.html
└── static/
├── style.css
└── script.js
