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

