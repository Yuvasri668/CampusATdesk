from flask import render_template, request, session

from models.application import Application
from models.category import Category
from models.company import Company
from models.job import Job
from utils.role_helpers import require_role

APPLICATION_STATUSES = ["Applied", "Shortlisted", "Interview Scheduled", "Rejected", "Hired"]


def register_student_application_routes(app):

    @app.route("/student/applications/filter")
    @require_role("student")
    def student_application_filter():
        user_id = session.get("user_id")
        status = request.args.get("status", "").strip()
        query = Application.query.filter_by(student_id=user_id)
        if status and status in APPLICATION_STATUSES:
            query = query.filter_by(status=status)
        applications = query.order_by(Application.created_at.desc()).all()
        return render_template(
            "student/application_filters.html",
            applications=applications,
            current_status=status,
            statuses=APPLICATION_STATUSES
        )

    @app.route("/student/jobs/category/<int:id>")
    @require_role("student")
    def student_jobs_by_category(id):
        category = Category.query.get_or_404(id)
        categories = [category]
        return render_template("student/jobs_by_category.html", categories=categories)

    @app.route("/student/jobs/company/<int:id>")
    @require_role("student")
    def student_jobs_by_company(id):
        company = Company.query.get_or_404(id)
        recruiter_ids = [r.id for r in company.recruiters]
        jobs = Job.query.filter(Job.posted_by.in_(recruiter_ids)).order_by(Job.created_at.desc()).all() if recruiter_ids else []
        return render_template("student/jobs_by_company.html", company=company, jobs=jobs)
