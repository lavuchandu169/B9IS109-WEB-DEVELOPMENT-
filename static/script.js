const apiBaseURL = 'http://127.0.0.1:5000';

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch(`${apiBaseURL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('token', data.token); // Store the token in local storage
            window.location.href = '/home'; // Redirect to home page
        } else {
            alert('Invalid login');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error logging in');
    });
}

function logout() {
    localStorage.removeItem('token'); // Remove the token from local storage
    window.location.href = '/'; // Redirect to home page
}

function addTask() {
    const taskText = document.getElementById('new-task').value;
    if (taskText) {
        fetch(`${apiBaseURL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // Include the token in the headers
            },
            body: JSON.stringify({ task: taskText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadTasks();
                document.getElementById('new-task').value = '';
            } else {
                alert('Error adding task');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding task');
        });
    }
}

function loadTasks() {
    fetch(`${apiBaseURL}/tasks`, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Include the token in the headers
        }
    })
    .then(response => response.json())
    .then(data => {
        const tasksList = document.getElementById('tasks');
        tasksList.innerHTML = '';
        data.tasks.forEach((task, index) => {
            const li = document.createElement('li');
            li.textContent = task;
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.onclick = () => deleteTask(index);
            li.appendChild(deleteButton);
            tasksList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading tasks');
    });
}

function deleteTask(index) {
    fetch(`${apiBaseURL}/tasks/${index}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}` // Include the token in the headers
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadTasks();
        } else {
            alert('Error deleting task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting task');
    });
}
