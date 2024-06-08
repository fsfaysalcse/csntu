from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/csndb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .views.user_views import user_views
    from .views.module_views import module_views
    from .views.assignment_views import assignment_views
    from .views.task_views import task_views
    from .views.main_views import main_views
    from .views.student_views import student_views  # Import the student_views blueprint

    app.register_blueprint(user_views, url_prefix='/users')
    app.register_blueprint(module_views, url_prefix='/modules')
    app.register_blueprint(assignment_views, url_prefix='/assignments')
    app.register_blueprint(task_views, url_prefix='/tasks')
    app.register_blueprint(main_views, url_prefix='/')
    app.register_blueprint(student_views)  # Register the student_views blueprint

    return app
