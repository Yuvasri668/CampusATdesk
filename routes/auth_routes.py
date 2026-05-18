from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from extensions import db
from models.user import User


def register_auth_routes(app):

    # =====================================================
    # REGISTER
    # =====================================================
    @app.route("/register", methods=["GET", "POST"])
    def register():

        # If already logged in
        if session.get("user_id"):
            return redirect(url_for("home"))

        if request.method == "POST":

            username = request.form.get(
                "username",
                ""
            ).strip()

            email = request.form.get(
                "email",
                ""
            ).strip()

            password = request.form.get(
                "password",
                ""
            )

            confirm_password = request.form.get(
                "confirm_password",
                ""
            )

            role = request.form.get(
                "role",
                ""
            )

            # =============================================
            # VALIDATIONS
            # =============================================

            if not username:
                flash("Username is required.", "error")
                return redirect(url_for("register"))

            if not email:
                flash("Email is required.", "error")
                return redirect(url_for("register"))

            if not password:
                flash("Password is required.", "error")
                return redirect(url_for("register"))

            if not confirm_password:
                flash("Confirm Password is required.", "error")
                return redirect(url_for("register"))

            if password != confirm_password:
                flash(
                    "Password and Confirm Password do not match.",
                    "error"
                )
                return redirect(url_for("register"))

            if not role:
                flash("Please select a role.", "error")
                return redirect(url_for("register"))

            # =============================================
            # CHECK EXISTING USER
            # =============================================

            if User.query.filter_by(username=username).first():
                flash("Username already exists.", "error")
                return redirect(url_for("register"))

            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "error")
                return redirect(url_for("register"))

            # =============================================
            # CREATE USER
            # =============================================

            user = User(
    username=username,
    email=email,
    password=generate_password_hash(password),
    role=role
)

            db.session.add(user)
            db.session.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(url_for("login"))

        return render_template("register.html")

    # =====================================================
    # LOGIN
    # =====================================================
    @app.route("/login", methods=["GET", "POST"])
    def login():

        # Already logged in
        if session.get("user_id"):
            return redirect(url_for("home"))

        if request.method == "POST":

            email = request.form.get(
                "email",
                ""
            ).strip()

            password = request.form.get(
                "password",
                ""
            )

            # =============================================
            # VALIDATION
            # =============================================

            if not email or not password:
                flash(
                    "Email and password are required.",
                    "error"
                )
                return redirect(url_for("login"))

            # =============================================
            # FIND USER
            # =============================================

            user = User.query.filter_by(email=email).first()

            if not user:
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            if not check_password_hash(
                user.password,
                password
            ):
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            # =============================================
            # CHECK ACCOUNT STATUS
            # =============================================

            if getattr(user, "is_active", True) is False:
                flash(
                    "Your account has been deactivated.",
                    "error"
                )
                return redirect(url_for("login"))

            # =============================================
            # CREATE SESSION
            # =============================================

            session["user_id"] = user.id
            session["user_role"] = user.role

            flash("Login successful.", "success")

            # =============================================
            # ROLE BASED REDIRECT
            # =============================================

            if user.role == "admin":
                return redirect(
                    url_for("admin_dashboard")
                )

            elif user.role == "recruiter":
                return redirect(
                    url_for("recruiter_dashboard")
                )

            elif user.role == "student":
                return redirect(
                    url_for("student_dashboard")
                )

            return redirect(url_for("home"))

        return render_template("login.html")

    # =====================================================
    # LOGOUT
    # =====================================================
    @app.route("/logout")
    def logout():

        session.pop("user_id", None)
        session.pop("user_role", None)

        flash(
            "You have been logged out.",
            "success"
        )

        return redirect(url_for("login"))