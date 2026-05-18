import os
import uuid
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename

from extensions import db
from models.job import Job
from models.application import Application
from utils.role_helpers import require_role

APPLICATION_STATUSES = ["Applied", "Shortlisted", "Interview Scheduled", "Rejected", "Hired"]
STATUS_FINAL = ["Rejected", "Hired"]
STATUS_WITHDRAWN = "Withdrawn"
STATUS_APPLIED = "Applied"


def allowed_resume(filename):
    from config import ALLOWED_RESUME_EXTENSIONS
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS


def register_job_application_routes(app):

    @app.route("/student/jobs/<int:job_id>/apply", methods=["GET", "POST"])
    @require_role("student")
    def student_job_apply(job_id):
        user_id = session.get("user_id")
        job = Job.query.get_or_404(job_id)
        existing = Application.query.filter_by(student_id=user_id, job_id=job_id).first()
        if existing:
            flash("You have already applied for this job.", "error")
            return redirect(url_for("student_applications"))
        if request.method == "POST":
            resume_path = None
            use_existing = request.form.get("use_existing_resume", "").strip()
            if use_existing and use_existing != "new":
                prev_app = Application.query.filter(
                    Application.id == int(use_existing),
                    Application.student_id == user_id,
                    Application.resume_path.isnot(None)
                ).first()
                if prev_app:
                    resume_path = prev_app.resume_path
            if resume_path is None:
                f = request.files.get("resume")
                if f and f.filename and allowed_resume(f.filename):
                    ext = f.filename.rsplit(".", 1)[1].lower()
                    name = f"{uuid.uuid4().hex}.{ext}"
                    path = os.path.join(current_app.config["UPLOAD_FOLDER"], name)
                    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                    f.save(path)
                    resume_path = name
                else:
                    flash("Please upload a resume (PDF, DOC, DOCX) or select an existing one.", "error")
                    return redirect(url_for("student_job_apply", job_id=job_id))
            app_record = Application(
                student_id=user_id,
                job_id=job_id,
                resume_path=resume_path,
                status=STATUS_APPLIED
            )
            db.session.add(app_record)
            db.session.commit()
            flash("Application submitted.", "success")
            return redirect(url_for("student_applications"))
        prev_apps = Application.query.filter(
            Application.student_id == user_id,
            Application.resume_path.isnot(None)
        ).order_by(Application.created_at.desc()).limit(20).all()
        return render_template(
            "student/job_apply.html",
            job=job,
            previous_applications=prev_apps
        )

    @app.route("/student/applications")
    @require_role("student")
    def student_applications():
        user_id = session.get("user_id")
        applications = Application.query.filter_by(student_id=user_id).order_by(Application.created_at.desc()).all()
        return render_template("student/applications.html", applications=applications)

    @app.route("/student/applications/<int:id>/edit", methods=["GET", "POST"])
    @require_role("student")
    def student_application_edit(id):
        user_id = session.get("user_id")
        application = Application.query.filter_by(id=id, student_id=user_id).first_or_404()
        if application.status in STATUS_FINAL or application.status == STATUS_WITHDRAWN:
            flash("This application cannot be edited.", "error")
            return redirect(url_for("student_applications"))
        if request.method == "POST":
            f = request.files.get("resume")
            if f and f.filename and allowed_resume(f.filename):
                ext = f.filename.rsplit(".", 1)[1].lower()
                name = f"{uuid.uuid4().hex}.{ext}"
                path = os.path.join(current_app.config["UPLOAD_FOLDER"], name)
                os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
                f.save(path)
                application.resume_path = name
                db.session.commit()
                flash("Resume updated.", "success")
            else:
                flash("Please upload a valid resume (PDF, DOC, DOCX).", "error")
            return redirect(url_for("student_applications"))
        return render_template("student/application_edit.html", application=application)

    @app.route("/student/applications/<int:id>/withdraw", methods=["POST"])
    @require_role("student")
    def student_application_withdraw(id):
        user_id = session.get("user_id")
        application = Application.query.filter_by(id=id, student_id=user_id).first_or_404()
        if application.status != STATUS_APPLIED:
            flash("You can only withdraw applications that are not yet processed.", "error")
            return redirect(url_for("student_applications"))
        application.status = STATUS_WITHDRAWN
        db.session.commit()
        flash("Application withdrawn.", "success")
        return redirect(url_for("student_applications"))
