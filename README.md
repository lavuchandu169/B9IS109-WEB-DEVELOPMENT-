# to-do-list-app
## To-Do List Web Application
### Introduction
The To-Do List Web Application is a simple web-based application developed using Flask and SQLite. It allows users to register, login, and manage their tasks efficiently. This application is designed to help users keep track of their daily tasks.

### Features
**User Registration:** Allows new users to create an account.

**User Login/Logout:** Secured login mechanism and the ability to logout.

**Task Management:** Users can add, view, edit, and delete their tasks.

**Role-Based Permissions:** Role-based user permissions to manage tasks.

### Technology Stack**
**Flask:** A micro web framework written in Python.

**SQLite:** A C library that implements an SQL database engine.

**HTML/CSS:** For structuring and styling the webpages.

**JavaScript** (Fetch API): For asynchronous operations and interaction with the backend.

### Project Structure

/to-do-list-app
|-- static/
|   |-- style.css # CSS styles used across the application
|   |-- script.js # JavaScript functions for front-end interactions
|-- templates/
|   |-- home.html # Homepage with login and register links
|   |-- login.html # Login page
|   |-- register.html # Registration page
|   |-- tasks.html # Task management page
|-- app.py # Flask application
|-- requirements.txt # Project dependencies
|-- README.md # Documentation


Setup and Installation
To get this project running on your local machine, follow these steps:

**Clone the repository:**

git clone https://github.com/lavuchandu169/to-do-list-app.git
Navigate into the project directory:

cd to-do-list-app
 **Create and activate a virtual environment:**

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
**Install dependencies:**

pip install -r requirements.txt
**Run the application:**

flask run
This will start the Flask server on http://localhost:5000.

**Usage**

Open your web browser and go to http://localhost:5000.
Register as a new user or login if you already have an account.
Navigate through the application to add, view, edit, or delete your tasks.
**Contributing**

Contributions to the To-Do List Web Application are welcome. Please follow these steps to contribute:

**Fork the repository.**

Create a new branch:
git checkout -b my-new-feature
Make your changes and commit them:

git commit -am 'Add some feature'
**Push to the branch:**

git push origin my-new-feature
Submit a pull request.

## License
This project is licensed under the MIT License.

## Author
Chandu Lavu


