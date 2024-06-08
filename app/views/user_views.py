from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, User

user_views = Blueprint('user_views', __name__)

@user_views.route('/')
def list_users():
    search = request.args.get('search', '')
    role = request.args.get('role', '')

    query = User.query
    if search:
        query = query.filter(User.name.ilike(f'%{search}%') | User.email.ilike(f'%{search}%'))
    if role:
        query = query.filter_by(role=int(role))

    users = query.all()
    return render_template('list_users.html', users=users)

@user_views.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('user_views.list_users'))

    return render_template('create_user.html')

@user_views.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']

        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('user_views.list_users'))

    return render_template('edit_user.html', user=user)

@user_views.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('user_views.list_users'))
