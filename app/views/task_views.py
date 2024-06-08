from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Task, User, Module

task_views = Blueprint('task_views', __name__)

@task_views.route('/')
def list_tasks():
    chapter_filter = request.args.get('chapter', '')
    student_id_filter = request.args.get('student_id', type=int)
    module_id_filter = request.args.get('module_id', type=int)

    query = Task.query

    if chapter_filter:
        query = query.filter(Task.chapter.ilike(f'%{chapter_filter}%'))
    if student_id_filter is not None:
        query = query.filter_by(student_id=student_id_filter)
    if module_id_filter is not None:
        query = query.filter_by(module_id=module_id_filter)

    tasks = query.all()

    students = User.query.filter_by(role=1).all()  # role=1 for Students
    modules = Module.query.all()

    # Convert to integers if present to avoid type errors in the template
    student_id_filter = student_id_filter or ''
    module_id_filter = module_id_filter or ''

    return render_template('list_tasks.html', tasks=tasks, students=students, modules=modules, student_id_filter=student_id_filter, module_id_filter=module_id_filter)

@task_views.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        chapter = request.form['chapter']
        student_id = request.form['student_id']
        module_id = request.form['module_id']
        task_type = request.form['task_type']
        mark = request.form['mark']
        total_mark = request.form['total_mark']

        new_task = Task(chapter=chapter, student_id=student_id, module_id=module_id, task_type=task_type, mark=mark, total_mark=total_mark)
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully!')
        return redirect(url_for('task_views.list_tasks'))

    students = User.query.filter_by(role=1).all()  # role=1 for Students
    modules = Module.query.all()
    return render_template('create_task.html', students=students, modules=modules)

@task_views.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.chapter = request.form['chapter']
        task.student_id = request.form['student_id']
        task.module_id = request.form['module_id']
        task.task_type = request.form['task_type']
        task.mark = request.form['mark']
        task.total_mark = request.form['total_mark']

        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('task_views.list_tasks'))

    students = User.query.filter_by(role=1).all()  # role=1 for Students
    modules = Module.query.all()
    return render_template('edit_task.html', task=task, students=students, modules=modules)

@task_views.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.')
    return redirect(url_for('task_views.list_tasks'))
