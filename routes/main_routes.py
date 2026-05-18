from flask import render_template, redirect, url_for, session

from utils.role_helpers import require_role


def register_main_routes(app):

    @app.route("/")
    def home():
        if not session.get("user_id"):
            return redirect(url_for("login"))
        role = session.get("user_role")
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        if role == "recruiter":
            return redirect(url_for("recruiter_dashboard"))
        if role == "student":
            return redirect(url_for("student_dashboard"))
        return redirect(url_for("login"))

    @app.route("/admin/jobs")
    @require_role("admin")
    def admin_jobs():
        return render_template("home.html")

    @app.route("/admin/applications")
    @require_role("admin")
    def admin_applications():
        return render_template("home.html")
