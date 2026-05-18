from flask import (
    render_template,
    session
)

from models.user import User
from models.job import Job
from models.application import Application

from utils.role_helpers import require_role


def register_recruiter_dashboard_routes(app):

    # =====================================================
    # RECRUITER DASHBOARD
    # =====================================================

    @app.route("/recruiter/dashboard")
    @require_role("recruiter")
    def recruiter_dashboard():

        user_id = session.get("user_id")

        user = User.query.get_or_404(user_id)

        # =============================================
        # GET RECRUITER JOBS
        # =============================================

        jobs = Job.query.filter_by(
            posted_by=user_id
        ).order_by(
            Job.created_at.desc()
        ).all()

        # =============================================
        # GET UNIQUE COMPANIES
        # =============================================

        companies = []

        for job in jobs:

            if job.company and job.company not in companies:
                companies.append(job.company)

        # =============================================
        # GET APPLICATIONS
        # =============================================

        job_ids = [job.id for job in jobs]

        applications = []

        if job_ids:

            applications = Application.query.filter(
                Application.job_id.in_(job_ids)
            ).order_by(
                Application.created_at.desc()
            ).all()

        return render_template(
            "recruiter/dashboard.html",
            companies=companies,
            jobs=jobs,
            applications=applications
        )

    # =====================================================
    # RECRUITER COMPANIES
    # =====================================================

    @app.route("/recruiter/companies")
    @require_role("recruiter")
    def recruiter_companies():

        user_id = session.get("user_id")

        jobs = Job.query.filter_by(
            posted_by=user_id
        ).all()

        companies = []

        for job in jobs:

            if job.company and job.company not in companies:
                companies.append(job.company)

        return render_template(
            "recruiter/companies.html",
            companies=companies
        )

    # =====================================================
    # RECRUITER APPLICATIONS
    # =====================================================

    @app.route("/recruiter/applications")
    @require_role("recruiter")
    def recruiter_applications():

        user_id = session.get("user_id")

        jobs = Job.query.filter_by(
            posted_by=user_id
        ).all()

        job_ids = [job.id for job in jobs]

        applications = []

        if job_ids:

            applications = Application.query.filter(
                Application.job_id.in_(job_ids)
            ).order_by(
                Application.created_at.desc()
            ).all()

        return render_template(
            "recruiter/applications.html",
            applications=applications
        )