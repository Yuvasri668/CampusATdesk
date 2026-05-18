from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from extensions import db

from models.user import User

from utils.role_helpers import require_role


def register_admin_routes(app):

    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    @app.route("/admin/dashboard")
    @require_role("admin")
    def admin_dashboard():

        users_count = User.query.count()

        recruiters_count = User.query.filter_by(
            role="recruiter"
        ).count()

        students_count = User.query.filter_by(
            role="student"
        ).count()

        return render_template(
            "admin_dashboard.html",
            users_count=users_count,
            recruiters_count=recruiters_count,
            students_count=students_count
        )

    # =====================================================
    # ALL USERS
    # =====================================================

    @app.route("/admin/users")
    @require_role("admin")
    def admin_users():

        users = User.query.order_by(
            User.created_at.desc()
        ).all()

        return render_template(
            "admin_users.html",
            users=users
        )

    # =====================================================
    # STUDENTS
    # =====================================================

    @app.route("/admin/students")
    @require_role("admin")
    def admin_students():

        students = User.query.filter_by(
            role="student"
        ).order_by(
            User.created_at.desc()
        ).all()

        return render_template(
            "admin_students.html",
            students=students
        )

    # =====================================================
    # ACTIVATE / DEACTIVATE STUDENT
    # =====================================================

    @app.route("/admin/students/status/<int:id>")
    @require_role("admin")
    def admin_student_status(id):

        student = User.query.get_or_404(id)

        # CHECK ROLE

        if student.role != "student":

            flash(
                "Only students allowed.",
                "error"
            )

            return redirect(
                url_for("admin_students")
            )

        # TOGGLE STATUS

        student.is_active = not student.is_active

        db.session.commit()

        flash(
            "Student status updated successfully.",
            "success"
        )

        return redirect(
            url_for("admin_students")
        )

    # =====================================================
    # DELETE STUDENT
    # =====================================================

    @app.route("/admin/students/delete/<int:id>")
    @require_role("admin")
    def admin_student_delete(id):

        student = User.query.get_or_404(id)

        # CHECK ROLE

        if student.role != "student":

            flash(
                "Only students can be deleted.",
                "error"
            )

            return redirect(
                url_for("admin_students")
            )

        # DELETE STUDENT

        db.session.delete(student)

        db.session.commit()

        flash(
            "Student deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin_students")
        )

    # =====================================================
    # DELETE RECRUITER
    # =====================================================

    @app.route("/admin/recruiters/delete/<int:id>")
    @require_role("admin")
    def admin_recruiter_delete(id):

        recruiter = User.query.get_or_404(id)

        # CHECK ROLE

        if recruiter.role != "recruiter":

            flash(
                "Only recruiters can be deleted.",
                "error"
            )

            return redirect(
                url_for("admin_recruiters")
            )

        # DELETE RECRUITER

        db.session.delete(recruiter)

        db.session.commit()

        flash(
            "Recruiter deleted successfully.",
            "success"
        )

        return redirect(
            url_for("admin_recruiters")
        )