from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

    tasks = db.relationship('Task', backref='owner', lazy=True)
    events = db.relationship('Event', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(100), nullable=False)
    end = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'success': False, 'message': 'Login failed! Please check your credentials and try again.'}), 401

        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True})

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists. Please choose a different username.'

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user_id = session['user_id']
    
    if request.method == 'POST':
        data = request.get_json()
        task_content = data['task']
        new_task = Task(task=task_content, user_id=current_user_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'success': True})

    user_tasks = Task.query.filter_by(user_id=current_user_id).all()
    return render_template('tasks.html', tasks=user_tasks)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    task_to_delete = Task.query.get_or_404(id)
    if task_to_delete.user_id != session['user_id']:
        return jsonify({'message': 'Permission denied!'})

    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    task_to_update = Task.query.get_or_404(id)
    if task_to_update.user_id != session['user_id']:
        return jsonify({'message': 'Permission denied!'})

    data = request.get_json()
    task_content = data['task']
    task_to_update.task = task_content
    db.session.commit()
    return jsonify({'success': True})

@app.route('/tasks/<int:id>/complete', methods=['PUT'])
def toggle_complete_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    task_to_toggle = Task.query.get_or_404(id)
    if task_to_toggle.user_id != session['user_id']:
        return jsonify({'message': 'Permission denied!'})

    task_to_toggle.complete = not task_to_toggle.complete
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/get-events', methods=['GET'])
def get_events():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    events = Event.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'start': event.start,
        'end': event.end
    } for event in events])

@app.route('/api/add-event', methods=['POST'])
def add_event():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    new_event = Event(
        title=data['title'],
        start=data['start'],
        end=data['end'],
        user_id=session['user_id']
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'success': True, 'event': {
        'id': new_event.id,
        'title': new_event.title,
        'start': new_event.start,
        'end': new_event.end
    }})

@app.route('/api/delete-event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != session['user_id']:
        return jsonify({'message': 'Permission denied!'})

    db.session.delete(event)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/update-event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    event = Event.query.get_or_404(event_id)
    if event.user_id != session['user_id']:
        return jsonify({'message': 'Permission denied!'})

    data = request.get_json()
    event.title = data['title']
    event.start = data['start']
    event.end = data['end']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/home')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

if __name__ == '__main__':
    if os.path.exists('site.db'):
        os.remove('site.db')
    db.create_all()
    app.run(debug=True)
