from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, LecturerModuleAssignment, User, Module

assignment_views = Blueprint('assignment_views', __name__)

@assignment_views.route('/assign', methods=['GET', 'POST'])
def assign_module():
    if request.method == 'POST':
        lecturer_id = request.form['lecturer_id']
        module_id = request.form['module_id']
        existing_assignment = LecturerModuleAssignment.query.filter_by(lecturer_id=lecturer_id, module_id=module_id).first()
        if existing_assignment:
            flash('This module is already assigned to the lecturer.')
        else:
            assignment = LecturerModuleAssignment(lecturer_id=lecturer_id, module_id=module_id)
            db.session.add(assignment)
            db.session.commit()
            flash('Module assigned to lecturer successfully.')
        return redirect(url_for('assignment_views.list_assignments'))

    lecturers = User.query.filter_by(role=2).all()
    modules = Module.query.all()
    return render_template('assign_module.html', lecturers=lecturers, modules=modules)

@assignment_views.route('/')
def list_assignments():
    lecturer_id = request.args.get('lecturer_id', type=int)
    search = request.args.get('search', type=str)
    
    query = LecturerModuleAssignment.query
    if lecturer_id:
        query = query.filter_by(lecturer_id=lecturer_id)
    if search:
        query = query.join(User).filter(User.name.ilike(f'%{search}%') | Module.name.ilike(f'%{search}%'))
    
    assignments = query.all()
    lecturers = User.query.filter_by(role=2).all()
    return render_template('list_assignments.html', assignments=assignments, lecturers=lecturers)

@assignment_views.route('/edit/<int:assignment_id>', methods=['GET', 'POST'])
def edit_assignment(assignment_id):
    assignment = LecturerModuleAssignment.query.get_or_404(assignment_id)
    if request.method == 'POST':
        assignment.lecturer_id = request.form['lecturer_id']
        assignment.module_id = request.form['module_id']
        db.session.commit()
        return redirect(url_for('assignment_views.list_assignments'))
    lecturers = User.query.filter_by(role=2).all()
    modules = Module.query.all()
    return render_template('edit_assignment.html', assignment=assignment, lecturers=lecturers, modules=modules)

@assignment_views.route('/delete/<int:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    assignment = LecturerModuleAssignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for('assignment_views.list_assignments'))
