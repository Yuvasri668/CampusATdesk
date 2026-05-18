from functools import wraps

from flask import session, redirect, url_for, flash


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please log in to access this page.", "error")
                return redirect(url_for("login"))
            if session.get("user_role") != role:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("home"))
            return f(*args, **kwargs)
        return wrapped
    return decorator
