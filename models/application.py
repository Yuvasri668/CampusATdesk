from datetime import datetime

from extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    resume_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Applied")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship("User", backref="applications", foreign_keys=[student_id])
    job = db.relationship("Job", backref="applications", foreign_keys=[job_id])
