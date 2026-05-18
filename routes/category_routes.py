from flask import render_template, request, redirect, url_for, flash

from extensions import db
from models.category import Category
from utils.role_helpers import require_role


def register_category_routes(app):

    @app.route("/admin/categories")
    @require_role("admin")
    def admin_categories():
        categories = Category.query.order_by(Category.name).all()
        return render_template("admin/categories.html", categories=categories)

    @app.route("/admin/categories/create", methods=["GET", "POST"])
    @require_role("admin")
    def admin_category_create():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Category name is required.", "error")
                return redirect(url_for("admin_category_create"))
            if Category.query.filter_by(name=name).first():
                flash("Category already exists.", "error")
                return redirect(url_for("admin_category_create"))
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash("Category created successfully.", "success")
            return redirect(url_for("admin_categories"))
        return render_template("admin/category_form.html", category=None)

    @app.route("/admin/categories/edit/<int:id>", methods=["GET", "POST"])
    @require_role("admin")
    def admin_category_edit(id):
        category = Category.query.get_or_404(id)
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Category name is required.", "error")
                return redirect(url_for("admin_category_edit", id=id))
            existing = Category.query.filter_by(name=name).first()
            if existing and existing.id != id:
                flash("Category name already exists.", "error")
                return redirect(url_for("admin_category_edit", id=id))
            category.name = name
            db.session.commit()
            flash("Category updated successfully.", "success")
            return redirect(url_for("admin_category_view", id=id))
        return render_template("admin/category_form.html", category=category)

    @app.route("/admin/categories/<int:id>")
    @require_role("admin")
    def admin_category_view(id):
        category = Category.query.get_or_404(id)
        return render_template("admin/category_view.html", category=category)
