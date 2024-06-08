from flask import Blueprint, render_template, request, redirect, url_for
from ..models import db, Module

module_views = Blueprint('module_views', __name__)

@module_views.route('/create', methods=['GET', 'POST'])
def create_module():
    if request.method == 'POST':
        module_code = request.form['module_code']
        name = request.form['name']
        description = request.form['description']
        module = Module(module_code=module_code, name=name, description=description)
        db.session.add(module)
        db.session.commit()
        return redirect(url_for('module_views.list_modules'))
    return render_template('create_module.html')

@module_views.route('/')
def list_modules():
    module_code = request.args.get('module_code', type=str)
    
    query = Module.query
    if module_code:
        query = query.filter(Module.module_code.ilike(f'%{module_code}%'))
    
    modules = query.all()
    return render_template('list_modules.html', modules=modules)

@module_views.route('/edit/<int:module_id>', methods=['GET', 'POST'])
def edit_module(module_id):
    module = Module.query.get_or_404(module_id)
    if request.method == 'POST':
        module.module_code = request.form['module_code']
        module.name = request.form['name']
        module.description = request.form['description']
        db.session.commit()
        return redirect(url_for('module_views.list_modules'))
    return render_template('edit_module.html', module=module)

@module_views.route('/delete/<int:module_id>', methods=['POST'])
def delete_module(module_id):
    module = Module.query.get_or_404(module_id)
    db.session.delete(module)
    db.session.commit()
    return redirect(url_for('module_views.list_modules'))
