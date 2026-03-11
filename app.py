
import os # <-- Add this import
from flask import Flask, render_template, request, redirect, session
from setup_db import db, User, Drive, Application

app = Flask(__name__)
# It's best practice to use an environment variable for secret keys in production too
app.secret_key = os.getenv("SECRET_KEY", "placement_portal_secret") 

# --- CHANGE YOUR DATABASE URI CONFIGURATION HERE ---
# This looks for a cloud database URL, but defaults to your local placement.db
db_url = os.getenv("DATABASE_URL", "sqlite:///placement.db")

# SQLAlchemy requires 'postgresql://' but some cloud hosts provide 'postgres://'. This fixes that automatically.
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ... (Keep the rest of your app.py exactly the same from the admin creation downwards) ...



with app.app_context():

    admin = User.query.filter_by(username="admin").first()

    if not admin:
        admin = User(
            username="admin",
            password="admin123",
            role="Admin",
            status="Approved"
        )

        db.session.add(admin)
        db.session.commit()
# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template("home.html")

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET','POST'])
def login():


    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(
            username=username,
            password=password,
            role=role
        ).first()

        if user:

            if user.status == "Blacklisted":
                 return "Your account has been blacklisted by Admin."


            if role == "Company" and user.status != "Approved":
                return f"Your account status is {user.status}"

            session['username'] = username
            session['role'] = role

            if role == "Admin":
                return redirect('/admin')

            elif role == "Company":
                return redirect('/company')

            else:
                return redirect('/student')

        else:
            return "Invalid login"

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET','POST'])
def register():


    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        department = request.form.get('department')
        overview = request.form.get('overview')

        status = "Pending" if role=="Company" else "Approved"

        new_user = User(
            username=username,
            password=password,
            role=role,
            department=department,
            overview=overview,
            status=status
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template("register.html")


# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -------------------------------ADMIN -------------------------------------

@app.route('/admin')
def admin_dashboard():


    if session.get('role') != "Admin":
        return redirect('/login')

    pending = User.query.filter_by(role="Company",status="Pending").all()
    approved = User.query.filter_by(role="Company",status="Approved").all()
    students = User.query.filter_by(role="Student",status="Approved").all()
    drives = Drive.query.filter_by(status="Ongoing").all()
    blacklisted = User.query.filter_by(status="Blacklisted").all()

    applications = db.session.query(
    Application.id,
    Application.student_username,
    Drive.drive_name,

    Drive.company_username,
    Drive.application_deadline
    ).join(Drive, Application.drive_id == Drive.id).all()
                                                     
    student_count = User.query.filter_by(role='Student').count()
    company_count = User.query.filter_by(role='Company').count()
    drive_count = Drive.query.filter_by(status="Ongoing").count()
    app_count = Application.query.count()
   
        
    return render_template(
                "admin_dashboard.html",
                pending=pending,
                approved=approved,
                students=students,
                drives=drives,
                applications=applications,
                blacklisted=blacklisted,
                total_students=student_count,
                total_companies=company_count,
                total_drives=drive_count,
                total_applications=app_count,
                
                username=session['username'])
#=======================================================================

@app.route('/approve_company/<username>')
def approve_company(username):
    user = User.query.filter_by(username=username).first()
    user.status = "Approved"

    db.session.commit()

    return redirect('/admin')


@app.route('/blacklist/<username>')
def blacklist(username):
    user = User.query.filter_by(username=username).first()
    user.status = "Blacklisted"

    db.session.commit()

    return redirect('/admin')

#=============================================================================


@app.route("/admin/application/<int:app_id>")
def admin_application_view(app_id):

    if 'username' not in session or session['role'] != 'Admin':
        return redirect('/login')

    data = db.session.query(
        Application.id.label("app_id"),
        Application.status,
        Application.drive_id,
        User.username.label("student_name"),
        User.department,
        Drive.drive_name,
        Drive.job_title
    ).join(User, Application.student_username == User.username)\
     .join(Drive, Application.drive_id == Drive.id)\
     .filter(Application.id == app_id).first()

    return render_template("admin_student_application.html", data=data)

#=================================================================================

    
@app.route("/admin_search")
def admin_search():
    if 'username' not in session or session['role'] != 'Admin':
        return redirect('/login')

    query = request.args.get("query")
    search_type = request.args.get("search_type")

    
    if search_type == "student":
        students = User.query.filter(User.role=="Student", User.username.like(f"%{query}%")).all()
        
        companies = User.query.filter_by(role="Company", status="Approved").all()

    elif search_type == "company":
        companies = User.query.filter(User.role=="Company", User.username.like(f"%{query}%")).all()
        
        students = User.query.filter_by(role="Student", status="Approved").all()

    else:
        
        students = User.query.filter_by(role="Student", status="Approved").all()
        companies = User.query.filter_by(role="Company", status="Approved").all()

    
    pending = User.query.filter_by(role="Company", status="Pending").all()
    drives = Drive.query.filter_by(status="Ongoing").all()
    blacklisted = User.query.filter_by(status="Blacklisted").all()

    applications = db.session.query(
        Application.id,
        Application.student_username,
        Drive.drive_name,
        Drive.company_username,
        Drive.application_deadline
    ).join(Drive, Application.drive_id == Drive.id).all()
                                                     
    student_count = User.query.filter_by(role='Student').count()
    company_count = User.query.filter_by(role='Company').count()
    drive_count = Drive.query.count()

    
    return render_template(
        "admin_dashboard.html",
        students=students,
        approved=companies,
        pending=pending,
        drives=drives,
        applications=applications,
        blacklisted=blacklisted,
        total_students=student_count,
        total_companies=company_count,
        total_drives=drive_count,
        username=session['username']
    )
    
#=======================================================================================
@app.route("/admin_action/<action>/<username>")
def admin_action(action, username):

    if session.get('role') != "Admin":
        return redirect('/login')

    user = User.query.filter_by(username=username).first()

    if action == "approve":
        user.status = "Approved"

    elif action == "blacklist":
        user.status = "Blacklisted"

    db.session.commit()

    return redirect("/admin")



@app.route("/unblacklist/<username>")
def unblacklist(username):

    if session.get('role') != "Admin":
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    user.status = "Approved"

    db.session.commit()

    return redirect("/admin")
#================================================================================

@app.route("/admin/drive/<int:drive_id>")
def admin_drive_view(drive_id):

    if 'username' not in session or session['role'] != 'Admin':
        return redirect('/login')

    drive = Drive.query.get(drive_id)

    return render_template(
        "admin_drive_details.html",
        drive=drive
    )


@app.route('/admin/approve/<int:app_id>')
def approve_application(app_id):

    application = Application.query.get(app_id)
    application.status = "Approved"

    db.session.commit()

    return redirect('/admin')


@app.route('/admin/reject/<int:app_id>')
def reject_application(app_id):

    application = Application.query.get(app_id)
    application.status = "Rejected"

    db.session.commit()

    return redirect('/admin')



@app.route('/admin/application/<int:app_id>')
def view_application(app_id):

    application = Application.query.get(app_id)

    return render_template("admin_student_application.html", data=application)




# --- Mark Drive as Complete ---
@app.route("/admin_action/complete_drive/<int:drive_id>")
def complete_drive_admin(drive_id):
    if session.get('role') != "Admin":
        return redirect('/login')

    
    drive = Drive.query.get(drive_id)
    
    if drive:
        drive.status = "Completed"
        db.session.commit() 
    
    return redirect('/admin')







# ------------------------------------ COMPANY ----------------------------------------------

@app.route('/company')
def company_dashboard():


    if session.get('role') != "Company":
        return redirect('/login')

    company = session['username']

    upcoming = Drive.query.filter_by(
        company_username=company,
        status="Ongoing"
    ).all()

    closed = Drive.query.filter_by(
        company_username=company,
        status="Completed"
    ).all()

    return render_template(
        "company_dashboard.html",
        upcoming=upcoming,
        closed=closed,
        username=session['username']
    )


@app.route('/create_drive', methods=['GET','POST'])
def create_drive():


    if session.get('role') != "Company":
        return redirect('/login')

    if request.method == "POST":

        drive = Drive(
            company_username=session['username'],
            drive_name=request.form['drive_name'],
            job_title=request.form['job_title'],
            description=request.form['description'],
            eligibility_criteria=request.form['eligibility_criteria'],
            application_deadline=request.form['application_deadline'],
            salary=request.form['salary'],
            status="Ongoing"
        )

        db.session.add(drive)
        db.session.commit()

        return redirect('/company')

    return render_template("create_drive.html")


@app.route("/drive_details/<int:drive_id>")
def drive_details(drive_id):

    if 'username' not in session or session['role'] != 'Company':
        return redirect('/login')

    drive = Drive.query.get(drive_id)

    applications = Application.query.filter_by(
        drive_id=drive_id
    ).all()

    return render_template(
        "drive_details.html",
        drive=drive,
        applications=applications
    )

@app.route("/review_application/<int:app_id>", methods=["GET","POST"])
def review_application(app_id):

    if 'username' not in session or session['role'] != 'Company':
        return redirect('/login')

    application = Application.query.get(app_id)
    student = User.query.filter_by(username=application.student_username).first()
    drive = Drive.query.get(application.drive_id)

    if request.method == "POST":
        application.status = request.form['status']
        db.session.commit()
        return redirect(f"/review_application/{app_id}")

    return render_template(
    "review_application.html",
    data={
        "student_name": student.username,
        "department": student.department,
        "drive_name": drive.drive_name,
        "job_title": drive.job_title,
        "status": application.status,
        "app_id": application.id,
        "drive_id": drive.id
    }
)

@app.route("/view_resume/<student_username>")
def view_resume(student_username):

    if 'username' not in session or session['role'] not in ['Company','Admin']:
        return redirect('/login')

    student = User.query.filter_by(username=student_username).first()

    return render_template("view_resume.html", student=student)


@app.route('/complete_drive/<int:id>')
def complete_drive(id):


    drive = Drive.query.get(id)
    drive.status = "Completed"

    db.session.commit()

    return redirect('/company')




# ----------------------------------- STUDENT ------------------------------------------

@app.route('/student')
def student_dashboard():


    if session.get('role') != "Student":
        return redirect('/login')

    companies = User.query.filter_by(
        role="Company",
        status="Approved"
    ).all()
    

    applied_drives = db.session.query(
        Drive.id,
        Drive.drive_name,
        Drive.company_username,
        Drive.application_deadline,
        Application.status
    ).join(Drive, Application.drive_id == Drive.id).filter(
        Application.student_username == session['username']
    ).all()

    return render_template(
        "student_dashboard.html",
        companies=companies,
        applied_drives=applied_drives,
        username=session['username']
    )

@app.route('/student/edit_profile', methods=['GET','POST'])
def student_edit_profile():


    if session.get('role') != "Student":
        return redirect('/login')

    user = User.query.filter_by(
        username=session['username']
    ).first()

    if request.method == "POST":

        user.name = request.form['name']
        user.department = request.form['department']
        user.cgpa = request.form['cgpa']
        user.skills = request.form['skills']
        user.projects = request.form['projects']
        user.achievements = request.form['achievements']
        db.session.commit()

        return redirect('/student')

    return render_template(
        "edit_profile.html",
        user=user
    )

@app.route('/student/history')
def student_history():


    if 'username' not in session or session['role'] != 'Student':
        return redirect('/login')

    username = session['username']

    user = User.query.filter_by(username=username).first()

    history = db.session.query(
        Application.status,
        Drive.id,
        Drive.job_title
    ).join(Drive).filter(
        Application.student_username == username
    ).all()

    return render_template(
        "student_history.html",
        username=username,
        department=user.department,
        history=history
    )

@app.route("/student/company/<company_username>")
def student_company_view(company_username):

    if 'username' not in session or session['role'] != 'Student':
        return redirect('/login')

    company = User.query.filter_by(username=company_username).first()

    drives = Drive.query.filter_by(
        company_username=company_username,
        status="Ongoing"
    ).all()

    return render_template(
        "company_details.html",
        company_name=company_username,
        company_data=company,
        drives=drives
    )

@app.route("/student/drive/<int:drive_id>")
def student_drive_view(drive_id):

    if 'username' not in session or session['role'] != 'Student':
        return redirect('/login')

    drive = Drive.query.get(drive_id)

    existing_app = Application.query.filter_by(
        student_username=session['username'],
        drive_id=drive_id
    ).first()

    has_applied = True if existing_app else False

    return render_template(
        "student_drive_details.html",
        drive=drive,
        has_applied=has_applied
    )



@app.route('/student/apply/<int:drive_id>')
def apply_drive(drive_id):


    if session.get('role') != "Student":
        return redirect('/login')

    app_data = Application(
        student_username=session['username'],
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(app_data)
    db.session.commit()

    return redirect('/student')




if __name__ == "__main__":
    app.run(debug=True)
