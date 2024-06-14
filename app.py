from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from datetime import datetime 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET"])
def homepage():
    return render_template('home.html')

@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f"{username} has entered the Task Manager, Welcome!", category='success')
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", category='error')
    return render_template("login.html")

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('homepage'))

@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if not username or not password or not email:
            flash("Username, password, and email cannot be empty", category='error')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash("Username already taken", category='error')
        elif User.query.filter_by(email=email).first():
            flash("Email already in use", category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("Your account has been created successfully", category='success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content, user_id=current_user.id)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully', category='success')
        except:
            flash('Error adding task', category='error')
        return redirect(url_for('home'))
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created).all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You are not authorized to delete this task', category='error')
        return redirect(url_for('home'))
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', category='success')
    except:
        flash('Error deleting task', category='error')
    return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You are not authorized to update this task', category='error')
        return redirect(url_for('home'))
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            flash('Task updated successfully', category='success')
            return redirect(url_for('home'))
        except:
            flash('Error updating task', category='error')
    return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)

'''
To initialize the database:
    python3
    >>> from app import db
    >>> db.create_all()
'''
