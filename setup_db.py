


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ---------------- USERS TABLE ----------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(50), nullable=False)

    status = db.Column(db.String(50), default="Pending")

    department = db.Column(db.String(100))
    overview = db.Column(db.Text)

    name = db.Column(db.String(100))
    cgpa = db.Column(db.String(10))
    skills = db.Column(db.Text)
    projects = db.Column(db.Text)
    achievements = db.Column(db.Text)

    github = db.Column(db.String(200))
    linkedin = db.Column(db.String(200))
    portfolio = db.Column(db.String(200))


# ---------------- DRIVES TABLE ----------------
class Drive(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company_username = db.Column(db.String(100), nullable=False)

    drive_name = db.Column(db.String(200), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)
    eligibility_criteria = db.Column(db.Text)
    application_deadline = db.Column(db.String(100))
    salary = db.Column(db.String(100))

    status = db.Column(db.String(50), default="Pending")


# ---------------- APPLICATION TABLE ----------------
class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_username = db.Column(db.String(100), nullable=False)

    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)

    drive = db.relationship("Drive", backref="applications")

    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(50), default="Applied")