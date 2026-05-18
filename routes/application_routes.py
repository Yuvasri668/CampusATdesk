import os

from flask import render_template, request, redirect, url_for, flash, session, current_app, send_from_directory

from extensions import db
from models.job import Job
from models.application import Application
from utils.role_helpers import require_role

APPLICATION_STATUSES = ["Applied", "Shortlisted", "Interview Scheduled", "Rejected", "Hired"]
STATUS_LOCKED = ["Rejected", "Hired"]


def register_application_routes(app):

    @app.route("/recruiter/jobs/<int:job_id>/applications")
    @require_role("recruiter")
    def recruiter_job_applications(job_id):
        user_id = session.get("user_id")
        job = Job.query.filter_by(id=job_id, posted_by=user_id).first_or_404()
        applications = Application.query.filter_by(job_id=job_id).order_by(Application.created_at.desc()).all()
        return render_template(
            "recruiter/applicants.html",
            job=job,
            applications=applications,
            statuses=APPLICATION_STATUSES
        )

    @app.route("/recruiter/applications/update-status/<int:id>", methods=["POST"])
    @require_role("recruiter")
    def recruiter_application_update_status(id):
        user_id = session.get("user_id")
        application = Application.query.get_or_404(id)
        job = Job.query.filter_by(id=application.job_id, posted_by=user_id).first_or_404()
        if application.status in STATUS_LOCKED:
            flash("This application status cannot be changed.", "error")
            return redirect(url_for("recruiter_job_applications", job_id=application.job_id))
        status = request.form.get("status", "").strip()
        if status not in APPLICATION_STATUSES:
            flash("Invalid status.", "error")
            return redirect(url_for("recruiter_job_applications", job_id=application.job_id))
        application.status = status
        db.session.commit()
        flash("Application status updated.", "success")
        return redirect(url_for("recruiter_job_applications", job_id=application.job_id))

    @app.route("/recruiter/applications/<int:id>/resume")
    @require_role("recruiter")
    def recruiter_application_resume(id):
        user_id = session.get("user_id")
        application = Application.query.get_or_404(id)
        job = Job.query.filter_by(id=application.job_id, posted_by=user_id).first_or_404()
        if not application.resume_path:
            flash("No resume attached to this application.", "error")
            return redirect(url_for("recruiter_job_applications", job_id=application.job_id))
        upload_folder = current_app.config["UPLOAD_FOLDER"]
        path = os.path.abspath(os.path.join(upload_folder, application.resume_path))
        if not path.startswith(os.path.abspath(upload_folder)) or not os.path.isfile(path):
            flash("Resume file not found.", "error")
            return redirect(url_for("recruiter_job_applications", job_id=application.job_id))
        return send_from_directory(
            upload_folder,
            application.resume_path,
            as_attachment=True,
            download_name=f"resume_application_{application.id}{os.path.splitext(application.resume_path)[1]}"
        )
