To-Do List Web Application
A simple To-Do List application built using Flask, SQLAlchemy, and JWT for authentication.

Features
User registration and login
JWT-based authentication
Task management (add, view, delete tasks)
Role-based user permissions
Technologies Used
Python
Flask
SQLAlchemy
Flask-Bcrypt
JWT
HTML/CSS
JavaScript (Fetch API)
Requirements
Python 3.7+
Virtual Environment
Installation
Clone the repository:

git clone https://github.com/lavuchandu169/to-do-list-app.git
cd to-do-list-app
Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
Install the required packages:

pip install -r requirements.txt
Run the application:

flask run
Open your browser and navigate to:

http://127.0.0.1:5000/
Usage
Register a New User
Navigate to the registration page from the home page.
Fill in the username and password fields.
Submit the form to create a new account.
Login
Navigate to the login page from the home page.
Fill in your username and password.
Submit the form to log in.
Manage Tasks
Add Task: Enter a new task in the input field and click "Add Task".
View Tasks: All tasks are displayed in a list.
Delete Task: Click the "Delete" button next to a task to remove it.
Project Structure
to-do-list-app/ │ ├── app.py ├── requirements.txt ├── templates/ │ ├── home.html │ ├── login.html │ ├── register.html │ └── index.html └── static/ ├── style.css └── script.js

API Endpoints
POST /login: User login
POST /register: User registration
GET /tasks: Get all tasks for the logged-in user
POST /tasks: Add a new task
DELETE /tasks/<id>: Delete a task by ID
Contributing
Contributions are welcome! Please create a pull request with a clear description of your changes.

License
This project is licensed under the MIT License.

Author
Chandu Lavu
