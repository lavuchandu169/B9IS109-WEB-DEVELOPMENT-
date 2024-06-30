from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress the warning
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            print("Token is missing!")
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['username']).first()
            print(f"Token valid for user: {data['username']}")
        except Exception as e:
            print(f"Token is invalid: {e}")
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 403
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        if not data or not data['username'] or not data['password']:
            return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return jsonify({'message': 'User not found!'}), 401

        if bcrypt.check_password_hash(user.password, data['password']):
            token = jwt.encode({'username': user.username, 'exp': datetime.datetime.now(pytz.UTC) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
            return jsonify({'token': token})

        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    return render_template('login.html')

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
@token_required
def tasks(current_user):
    if request.method == 'POST':
        task_content = request.get_json()['task']
        new_task = Task(task=task_content, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'success': True, 'task': new_task.task})
    
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify({'tasks': [task.task for task in user_tasks]})

@app.route('/tasks/<int:id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):
    task_to_delete = Task.query.get_or_404(id)
    if task_to_delete.user_id != current_user.id:
        return jsonify({'message': 'Permission denied!'})
    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/home')
@token_required
def index(current_user):
    return render_template('index.html', username=current_user.username)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

