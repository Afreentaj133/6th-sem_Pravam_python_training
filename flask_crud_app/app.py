from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_crud_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not name or not email or not password or not confirm_password:
            flash('Please fill in all fields.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email is already registered.', 'warning')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as err:
            db.session.rollback()
            flash(f'Database error: {err}', 'danger')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')

        session.clear()
        session['user_id'] = user.id
        session['user_name'] = user.name
        flash('Login successful.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('login.html')


def login_required(view_func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access that page.', 'warning')
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)

    wrapper.__name__ = view_func.__name__
    return wrapper


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/students')
@login_required
def students():
    search_term = request.args.get('search', '').strip()
    
    if search_term:
        student_list = Student.query.filter(
            (Student.name.ilike(f'%{search_term}%')) |
            (Student.email.ilike(f'%{search_term}%')) |
            (Student.course.ilike(f'%{search_term}%')) |
            (Student.phone.ilike(f'%{search_term}%'))
        ).all()
    else:
        student_list = Student.query.all()

    return render_template('students.html', students=student_list, search_term=search_term)


@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip().lower()
        course = request.form.get('course').strip()
        phone = request.form.get('phone').strip()
        is_active = 1 if request.form.get('is_active') == 'on' else 0

        if not name or not email or not course or not phone:
            flash('All fields are required.', 'danger')
            return render_template('add_student.html')

        try:
            new_student = Student(name=name, email=email, course=course, phone=phone, is_active=bool(is_active))
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully.', 'success')
            return redirect(url_for('students'))
        except Exception as err:
            db.session.rollback()
            flash(f'Database error: {err}', 'danger')

    return render_template('add_student.html')


@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    student = Student.query.get(student_id)

    if not student:
        flash('Student not found.', 'warning')
        return redirect(url_for('students'))

    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip().lower()
        course = request.form.get('course').strip()
        phone = request.form.get('phone').strip()
        is_active = 1 if request.form.get('is_active') == 'on' else 0

        if not name or not email or not course or not phone:
            flash('All fields are required.', 'danger')
            return render_template('edit_student.html', student=student)

        try:
            student.name = name
            student.email = email
            student.course = course
            student.phone = phone
            student.is_active = bool(is_active)
            db.session.commit()
            flash('Student updated successfully.', 'success')
            return redirect(url_for('students'))
        except Exception as err:
            db.session.rollback()
            flash(f'Database error: {err}', 'danger')

    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    student = Student.query.get(student_id)

    if student:
        try:
            db.session.delete(student)
            db.session.commit()
            flash('Student deleted successfully.', 'success')
        except Exception as err:
            db.session.rollback()
            flash(f'Database error: {err}', 'danger')
    else:
        flash('Student not found.', 'warning')

    return redirect(url_for('students'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
