from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, nullable=False)  # 1 for Student, 2 for Teacher

    def __repr__(self):
        return f'<User {self.name}>'

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    cover_image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Module {self.module_code} - {self.name}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # Quiz, Homework, Exam
    mark = db.Column(db.Float, nullable=False)
    total_mark = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    student = db.relationship('User', backref=db.backref('tasks', lazy=True))
    module = db.relationship('Module', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f'<Task {self.chapter} - {self.task_type}>'

class LecturerModuleAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

    lecturer = db.relationship('User', backref=db.backref('lecturer_assignments', lazy=True))
    module = db.relationship('Module', backref=db.backref('module_assignments', lazy=True))

    def __repr__(self):
        return f'<LecturerModuleAssignment {self.lecturer_id} - {self.module_id}>'
