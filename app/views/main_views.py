from flask import Blueprint, render_template, jsonify
from ..models import db, Task, User, Module, LecturerModuleAssignment

main_views = Blueprint('main_views', __name__)

@main_views.route('/')
def index():
    return render_template('homepage.html')

@main_views.route('/counts-data')
def counts_data():
    total_users = User.query.count()
    total_students = User.query.filter_by(role=1).count()  # role=1 for Students
    total_teachers = User.query.filter_by(role=2).count()  # role=2 for Teachers
    modules = db.session.query(Module).count()
    tasks = Task.query.count()

    data = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'modules': modules,
        'tasks': tasks
    }
    return jsonify(data)

@main_views.route('/module-performance-data')
def module_performance_data():
    modules = Module.query.all()
    data = []
    for module in modules:
        lecturer_assignment = LecturerModuleAssignment.query.filter_by(module_id=module.id).first()
        lecturer_name = lecturer_assignment.lecturer.name if lecturer_assignment else 'N/A'

        tasks = Task.query.filter_by(module_id=module.id).all()
        total_tasks = len(tasks)
        total_marks = sum(task.mark for task in tasks)
        total_max_marks = sum(task.total_mark for task in tasks)
        average_marks = (total_marks / total_tasks) if total_tasks > 0 else 0

        passing_tasks = sum(1 for task in tasks if task.mark >= task.total_mark * 0.5)
        failing_tasks = total_tasks - passing_tasks

        data.append({
            'module_name': module.name,
            'lecturer_name': lecturer_name,
            'total_students': len(set(task.student_id for task in tasks)),
            'average_marks': average_marks,
            'total_marks': total_marks,
            'total_max_marks': total_max_marks,
            'passing_rate': (passing_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
            'failing_rate': (failing_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        })

    return jsonify(data)
