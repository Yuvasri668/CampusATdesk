from flask import render_template, session

from models.user import User
from models.company import Company
from models.category import Category
from models.application import Application
from utils.role_helpers import require_role


def register_student_dashboard_routes(app):

    @app.route("/student/dashboard")
    @require_role("student")
    def student_dashboard():
        user_id = session.get("user_id")
        user = User.query.get_or_404(user_id)
        applications = Application.query.filter_by(student_id=user_id).order_by(Application.created_at.desc()).all()
        upcoming_interviews = Application.query.filter_by(
            student_id=user_id,
            status="Interview Scheduled"
        ).order_by(Application.created_at.desc()).all()
        return render_template(
            "student/dashboard.html",
            user=user,
            applications=applications,
            upcoming_interviews=upcoming_interviews
        )

    @app.route("/student/companies")
    @require_role("student")
    def student_companies():
        companies = Company.query.order_by(Company.name).all()
        return render_template("student/companies.html", companies=companies)

    @app.route("/student/jobs")
    @require_role("student")
    def student_jobs():
        categories = Category.query.order_by(Category.name).all()
        return render_template("student/jobs_by_category.html", categories=categories)

