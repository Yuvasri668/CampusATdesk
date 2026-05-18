from flask import Flask

from config import SECRET_KEY, DEBUG, DATABASE_URI
from extensions import db
from models.user import User
from models.category import Category
from models.company import Company
from models.job import Job
from models.application import Application
from routes.main_routes import register_main_routes
from routes.auth_routes import register_auth_routes
from routes.admin_routes import register_admin_routes
from routes.category_routes import register_category_routes
from routes.company_routes import register_company_routes
from routes.recruiter_routes import register_recruiter_routes
from routes.recruiter_dashboard_routes import register_recruiter_dashboard_routes
from routes.job_routes import register_job_routes
from routes.application_routes import register_application_routes
from routes.student_dashboard_routes import register_student_dashboard_routes
from routes.job_application_routes import register_job_application_routes
from routes.student_application_routes import register_student_application_routes
from mail_config import mail


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = DEBUG
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    from config import UPLOAD_FOLDER
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    register_main_routes(app)
    register_auth_routes(app)
    register_admin_routes(app)
    register_category_routes(app)
    register_company_routes(app)
    register_recruiter_routes(app)
    register_recruiter_dashboard_routes(app)
    register_job_routes(app)
    register_application_routes(app)
    register_student_dashboard_routes(app)
    register_job_application_routes(app)
    register_student_application_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=DEBUG, port=5001)
