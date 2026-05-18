from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from extensions import db

from models.job import Job
from models.category import Category
from models.company import Company

from utils.role_helpers import require_role


def register_job_routes(app):

    # =====================================================
    # RECRUITER JOB LIST
    # =====================================================

    @app.route("/recruiter/jobs")
    @require_role("recruiter")
    def recruiter_jobs():

        user_id = session.get("user_id")

        jobs = Job.query.filter_by(
            posted_by=user_id
        ).order_by(
            Job.created_at.desc()
        ).all()

        return render_template(
            "recruiter/jobs.html",
            jobs=jobs
        )

    # =====================================================
    # CREATE JOB
    # =====================================================

    @app.route(
        "/recruiter/jobs/create",
        methods=["GET", "POST"]
    )
    @require_role("recruiter")
    def recruiter_job_create():

        if request.method == "POST":

            title = request.form.get(
                "title",
                ""
            ).strip()

            description = request.form.get(
                "description",
                ""
            ).strip() or None

            required_skills = request.form.get(
                "required_skills",
                ""
            ).strip() or None

            location = request.form.get(
                "location",
                ""
            ).strip() or None

            job_type = request.form.get(
                "job_type",
                ""
            ).strip() or None

            category_id = request.form.get(
                "category_id",
                type=int
            ) or None

            company_id = request.form.get(
                "company_id",
                type=int
            ) or None

            # =============================================
            # VALIDATION
            # =============================================

            if not title:

                flash(
                    "Job title is required.",
                    "error"
                )

                return redirect(
                    url_for("recruiter_job_create")
                )

            if not company_id:

                flash(
                    "Please select a company.",
                    "error"
                )

                return redirect(
                    url_for("recruiter_job_create")
                )

            # =============================================
            # CREATE JOB
            # =============================================

            job = Job(
                title=title,
                description=description,
                required_skills=required_skills,
                location=location,
                job_type=job_type,
                category_id=category_id,
                company_id=company_id,
                posted_by=session.get("user_id")
            )

            db.session.add(job)
            db.session.commit()

            flash(
                "Job created successfully.",
                "success"
            )

            return redirect(
                url_for("recruiter_jobs")
            )

        # =============================================
        # LOAD FORM DATA
        # =============================================

        categories = Category.query.order_by(
            Category.name
        ).all()

        companies = Company.query.order_by(
            Company.name
        ).all()

        return render_template(
            "recruiter/job_form.html",
            job=None,
            categories=categories,
            companies=companies
        )

    # =====================================================
    # VIEW SINGLE JOB
    # =====================================================

    @app.route("/recruiter/jobs/<int:id>")
    @require_role("recruiter")
    def recruiter_job_view(id):

        user_id = session.get("user_id")

        job = Job.query.filter_by(
            id=id,
            posted_by=user_id
        ).first_or_404()

        return render_template(
            "recruiter/job_view.html",
            job=job
        )