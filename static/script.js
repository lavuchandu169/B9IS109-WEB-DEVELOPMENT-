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
        if (data.success) {
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
    fetch(`${apiBaseURL}/logout`, {
        method: 'POST'
    })
    .then(() => {
        window.location.href = '/'; // Redirect to home page
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error logging out');
    });
}

function addTask() {
    const taskText = document.getElementById('new-task').value;
    if (taskText) {
        fetch(`${apiBaseURL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: taskText })
        })
        .then(response => {
            if (response.ok) {
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
    fetch(`${apiBaseURL}/tasks`)
    .then(response => response.text())
    .then(html => {
        console.log('Tasks loaded:', html); // Log the loaded tasks HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const tasksList = doc.getElementById('tasks').innerHTML;
        document.getElementById('tasks').innerHTML = tasksList;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error loading tasks');
    });
}

function editTask(id, oldText) {
    const newText = prompt('Edit task:', oldText);
    if (newText) {
        fetch(`${apiBaseURL}/tasks/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task: newText })
        })
        .then(response => {
            if (response.ok) {
                loadTasks();
            } else {
                alert('Error editing task');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error editing task');
        });
    }
}

function toggleCompleteTask(id) {
    fetch(`${apiBaseURL}/tasks/${id}/complete`, {
        method: 'PUT'
    })
    .then(response => {
        if (response.ok) {
            loadTasks();
        } else {
            alert('Error toggling task');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error toggling task');
    });
}

function deleteTask(id) {
    fetch(`${apiBaseURL}/tasks/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
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

function filterTasks(filter) {
    const tasksList = document.getElementById('tasks').children;
    for (let i = 0; i < tasksList.length; i++) {
        const task = tasksList[i];
        if (filter === 'all') {
            task.style.display = 'flex';
        } else if (filter === 'complete' && task.classList.contains('completed')) {
            task.style.display = 'flex';
        } else if (filter === 'incomplete' && !task.classList.contains('completed')) {
            task.style.display = 'flex';
        } else {
            task.style.display = 'none';
        }
    }
}

function searchTasks() {
    const query = document.getElementById('search').value.toLowerCase();
    const tasksList = document.getElementById('tasks').children;
    for (let i = 0; i < tasksList.length; i++) {
        const task = tasksList[i];
        if (task.textContent.toLowerCase().includes(query)) {
            task.style.display = 'flex';
        } else {
            task.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', loadTasks);
