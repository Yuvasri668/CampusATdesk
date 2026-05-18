from flask import render_template, request, redirect, url_for, flash

from extensions import db
from models.user import User
from models.company import Company
from werkzeug.security import generate_password_hash
from utils.role_helpers import require_role


def register_recruiter_routes(app):

    @app.route("/admin/recruiters")
    @require_role("admin")
    def admin_recruiters():
        recruiters = User.query.filter_by(role="recruiter").order_by(User.created_at.desc()).all()
        return render_template("admin/recruiters.html", recruiters=recruiters)

    @app.route("/admin/recruiters/create", methods=["GET", "POST"])
    @require_role("admin")
    def admin_recruiter_create():
        companies = Company.query.order_by(Company.name).all()
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            company_id = request.form.get("company_id", type=int) or None
            if not username:
                flash("Username is required.", "error")
                return redirect(url_for("admin_recruiter_create"))
            if not email:
                flash("Email is required.", "error")
                return redirect(url_for("admin_recruiter_create"))
            if not password:
                flash("Password is required.", "error")
                return redirect(url_for("admin_recruiter_create"))
            if password != confirm_password:
                flash("Password and Confirm Password do not match.", "error")
                return redirect(url_for("admin_recruiter_create"))
            if User.query.filter_by(username=username).first():
                flash("Username already exists.", "error")
                return redirect(url_for("admin_recruiter_create"))
            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "error")
                return redirect(url_for("admin_recruiter_create"))
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role="recruiter",
                company_id=company_id,
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
            flash("Recruiter created successfully.", "success")
            return redirect(url_for("admin_recruiters"))
        return render_template("admin/recruiter_form.html", recruiter=None, companies=companies)

    @app.route("/admin/recruiters/edit/<int:id>", methods=["GET", "POST"])
    @require_role("admin")
    def admin_recruiter_edit(id):
        recruiter = User.query.filter_by(id=id, role="recruiter").first_or_404()
        companies = Company.query.order_by(Company.name).all()
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            company_id = request.form.get("company_id", type=int) or None
            if not username:
                flash("Username is required.", "error")
                return redirect(url_for("admin_recruiter_edit", id=id))
            existing = User.query.filter_by(username=username).first()
            if existing and existing.id != id:
                flash("Username already exists.", "error")
                return redirect(url_for("admin_recruiter_edit", id=id))
            recruiter.username = username
            recruiter.company_id = company_id
            db.session.commit()
            flash("Recruiter updated successfully.", "success")
            return redirect(url_for("admin_recruiters"))
        return render_template("admin/recruiter_form.html", recruiter=recruiter, companies=companies)

    @app.route("/admin/recruiters/status/<int:id>")
    @require_role("admin")
    def admin_recruiter_status(id):
        recruiter = User.query.filter_by(id=id, role="recruiter").first_or_404()
        recruiter.is_active = not recruiter.is_active
        db.session.commit()
        flash("Recruiter {} successfully.".format("activated" if recruiter.is_active else "deactivated"), "success")
        return redirect(url_for("admin_recruiters"))
