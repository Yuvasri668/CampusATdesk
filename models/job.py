from datetime import datetime

from extensions import db


class Job(db.Model):

    __tablename__ = "jobs"

    # =====================================================
    # TABLE COLUMNS
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    required_skills = db.Column(
        db.String(500),
        nullable=True
    )

    location = db.Column(
        db.String(200),
        nullable=True
    )

    job_type = db.Column(
        db.String(100),
        nullable=True
    )

    # =====================================================
    # CATEGORY RELATION
    # =====================================================

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    # =====================================================
    # COMPANY RELATION
    # =====================================================

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=True
    )

    # =====================================================
    # USER WHO POSTED JOB
    # =====================================================

    posted_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # =====================================================
    # CREATED DATE
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    category = db.relationship(
        "Category",
        backref="jobs",
        foreign_keys=[category_id]
    )

    company = db.relationship(
        "Company",
        backref="jobs",
        foreign_keys=[company_id]
    )

    poster = db.relationship(
        "User",
        backref="posted_jobs",
        foreign_keys=[posted_by]
    )