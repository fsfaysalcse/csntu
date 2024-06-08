from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Module, Task,LecturerModuleAssignment
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/csndb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = int(request.form['role'])
        user = User(name=name, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_user.html')

@app.route('/create_module', methods=['GET', 'POST'])
def create_module():
    if request.method == 'POST':
        module_code = request.form['module_code']
        name = request.form['name']
        description = request.form['description']
        file = request.files['cover_image']
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        module = Module(module_code=module_code, name=name, description=description, cover_image=filename)
        db.session.add(module)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_module.html')


@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        chapter = request.form['chapter']
        student_id = int(request.form['student_id'])
        module_id = int(request.form['module_id'])
        task_type = request.form['task_type']
        mark = float(request.form['mark'])
        total_mark = float(request.form['total_mark'])
        task = Task(chapter=chapter, student_id=student_id, module_id=module_id, task_type=task_type, mark=mark, total_mark=total_mark)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    students = User.query.filter_by(role=1).all()  # Only students
    modules = Module.query.all()
    return render_template('create_task.html', students=students, modules=modules)


@app.route('/assign_module', methods=['GET', 'POST'])
def assign_module():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']
        module_id = request.form['module_id']
        
        # Check if the assignment already exists
        existing_assignment = LecturerModuleAssignment.query.filter_by(lecturer_id=lecturer_id, module_id=module_id).first()
        if existing_assignment:
            flash('This module is already assigned to the lecturer.')
        else:
            assignment = LecturerModuleAssignment(lecturer_id=lecturer_id, module_id=module_id)
            db.session.add(assignment)
            db.session.commit()
            flash('Module assigned to lecturer successfully.')
        
        return redirect(url_for('index'))
    
    lecturers = User.query.filter_by(role=2).all()  # Assuming role 2 is for teachers
    modules = Module.query.all()
    return render_template('assign_module.html', lecturers=lecturers, modules=modules)



@app.route('/')
def index():
    users = User.query.all()
    modules = Module.query.all()
    tasks = Task.query.all()
    assignments = LecturerModuleAssignment.query.all()  # Query assignments
    return render_template('index.html', users=users, modules=modules, tasks=tasks, assignments=assignments)


if __name__ == '__main__':
    app.run(debug=True)
