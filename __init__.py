from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)

    db_path = os.path.join(os.getcwd(), "DevWebProjet", "db.sqlite")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SECURITY_PASSWORD_SALT'] = 'un_salt_securise'

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'asumakino@gmail.com'
    app.config['MAIL_PASSWORD'] = 'nvyn evsn rogu toqt'
    app.config['MAIL_DEFAULT_SENDER'] = 'asumakino@gmail.com'
    app.config['UPLOAD_FOLDER'] = 'static/uploads' 

    mail.init_app(app)
    db.init_app(app)

    from .models import User
    
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    from .manage_object import manage_object as manage_object_blueprint, b64encode_filter
    app.register_blueprint(manage_object_blueprint)
    app.jinja_env.filters['b64encode'] = b64encode_filter

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.jinja_env.filters['b64encode'] = b64encode_filter

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.jinja_env.filters['b64encode'] = b64encode_filter

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    app.jinja_env.filters['b64encode'] = b64encode_filter

    return app