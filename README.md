# 📌 Placement Portal - Campus Recruitment Management System

A comprehensive web-based platform designed to streamline and automate campus recruitment activities. The Placement Portal connects students, companies, and administrators in a centralized system to manage job placements efficiently.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Database Schema](#database-schema)
- [User Roles & Functions](#user-roles--functions)
- [Installation & Setup](#installation--setup)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)

---

## 🎯 Overview

The Placement Portal is an end-to-end recruitment management system built for educational institutions. It automates the placement process by providing:

- **For Students**: Browse job drives, submit applications, track application status, and manage their professional profiles
- **For Companies**: Post recruitment drives, define eligibility criteria, review student applications, and manage hiring timelines
- **For Administrators**: Manage all platform activities, approve/reject companies, oversee applications, and maintain system integrity

This system eliminates manual paperwork and creates a transparent, efficient recruitment workflow.

---

## 🚀 Key Features

### Student Features
- **User Registration & Authentication**: Secure login with role-based access
- **Complete Profile Management**: Upload resume, CGPA, skills, projects, achievements, and social profiles (LinkedIn, GitHub, Portfolio)
- **Drive Discovery**: Browse all active recruitment drives with complete job details
- **Application Submission**: Apply to multiple drives with a single click
- **Application Tracking**: View real-time status of submitted applications (Applied, Shortlisted, Waiting, or Rejected)
- **Drive History**: Access past and current application records
- **Resume Download**: Retrieve saved resumes and profile information

### Company Features
- **Company Registration**: Create company account with pending approval status
- **Profile Management**: Update company overview and details
- **Recruitment Drive Creation**: Post new drives with job title, description, eligibility criteria, salary, and application deadline
- **Application Management**: View all student applications for company drives
- **Application Status Updates**: Accept/reject student applications
- **Drive Management**: Create and manage multiple recruitment drives simultaneously

### Administrator Features
- **Dashboard Analytics**: View system-wide statistics (total students, companies, drives, applications)
- **User Management**: 
  - Approve or reject pending company registrations
  - Manage student accounts
  - Blacklist users if needed
- **Compliance Monitoring**: Track all applications and company activities
- **System Oversight**: View all recruitment drives and manage platform data integrity
- **Blacklist Management**: Maintain a blacklist of users for policy violations

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python Web Framework)
  - Lightweight and flexible micro-framework
  - Built-in routing, templating, and session management
  - RESTful route handling for different user roles
- **Python Version**: 3.x

### Database
- **Primary Database**: SQLite
  - Lightweight, serverless relational database
  - Perfect for application prototyping and small-to-medium deployments
  - File-based storage (placement.db)
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
  - Object-relational mapping for Python
  - Database abstraction layer
  - Built-in query support and relationships

### Frontend
- **HTML5**: Structure and semantic markup for all pages
- **CSS3**: Styling for responsive design and user interface
- **Templating**: Jinja2 (integrated with Flask)
  - Dynamic template rendering
  - Variable interpolation and control flow

### Additional Libraries
- **package**: Flask
- **package**: Flask-SQLAlchemy (Database ORM)
- **package**: Session Management (built into Flask)

### Development & Version Control
- **Version Control**: Git & GitHub
- **Development Environment**: Python virtual environment

---

## 🏗️ Project Architecture

The application follows a three-tier architecture:

```
┌─────────────────────────────────────────┐
│         Frontend Layer                  │
│   (HTML/CSS Templates - Jinja2)         │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Application Layer               │
│   (Flask Routes + Business Logic)       │
│         - Authentication                │
│         - Role-based access control     │
│         - Session management            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Data Layer                      │
│   (SQLAlchemy ORM)                      │
│   ↓                                     │
│   SQLite Database (placement.db)        │
└─────────────────────────────────────────┘
```

---

## 📊 Database Schema

### Users Table
Stores information for all platform users (Students, Companies, Admins)

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `username` | String | Unique identifier for login |
| `password` | String | User password |
| `role` | String | User type: Admin, Company, or Student |
| `status` | String | Account status: Approved, Pending, or Blacklisted |
| `department` | String | Student department or company type |
| `overview` | Text | Bio for companies or resume summary for students |
| `name` | String | Full name (Student) |
| `cgpa` | String | Academic performance (Student) |
| `skills` | Text | Technical skills (Student) |
| `projects` | Text | Project portfolio (Student) |
| `achievements` | Text | Awards and achievements (Student) |
| `github` | String | GitHub profile URL (Student) |
| `linkedin` | String | LinkedIn profile URL (Student) |
| `portfolio` | String | Portfolio website URL (Student) |

### Drives Table
Stores recruitment drive information posted by companies

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `company_username` | String | Company that posted the drive |
| `drive_name` | String | Name of the recruitment drive |
| `job_title` | String | Position title (e.g., Software Engineer) |
| `description` | Text | Detailed job description |
| `eligibility_criteria` | Text | Requirements for students (CGPA, skills, etc.) |
| `application_deadline` | String | Last date to apply |
| `salary` | String | Offered salary/package |
| `status` | String | Drive status: Ongoing or Closed |

### Applications Table
Tracks student applications to recruitment drives

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `student_username` | String | Student who applied |
| `drive_id` | Integer | Reference to Drives table |
| `application_date` | DateTime | When the application was submitted |
| `status` | String | Application status: Applied, Shortlisted, Waiting, or Rejected |

---

## 👥 User Roles & Functions

### 1. **Admin**
- **Access Level**: Full system access
- **Key Responsibilities**:
  - Approve or reject company registrations
  - Monitor all recruitment activities
  - Manage user accounts and blacklist violators
  - View system-wide analytics and reports
  - Ensure compliance with platform policies
- **Default Credentials**: Username: `admin` | Password: `admin123`

### 2. **Company**
- **Access Level**: Limited to company-specific functions
- **Key Responsibilities**:
  - Create and manage recruitment drives
  - Review and respond to student applications
  - Update company profile information
  - Track application pipeline and hiring progress
- **Account Status**: Requires admin approval before accessing full features

### 3. **Student**
- **Access Level**: Student-specific features only
- **Key Responsibilities**:
  - Create and maintain personal profile
  - Browse active recruitment drives
  - Apply for jobs matching their qualifications
  - Track application status in real-time
  - Update resume and professional information

---

## 💾 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Placement_portal_24F3002918
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
python setup_db.py
```
This creates the SQLite database and adds a default admin user.

---

## 📁 Project Structure

```
Placement_portal_24F3002918/
│
├── app.py                          # Main Flask application file with all routes
├── setup_db.py                     # Database initialization and models (SQLAlchemy)
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
│
├── templates/                      # HTML templates (Jinja2)
│   ├── home.html                  # Landing page
│   ├── login.html                 # Authentication page
│   ├── register.html              # User registration
│   ├── edit_profile.html          # Profile management
│   │
│   ├── student_dashboard.html     # Student main dashboard
│   ├── student_drive_details.html # Drive details for students
│   ├── student_history.html       # Application history
│   ├── review_application.html    # Application review
│   ├── view_resume.html           # Resume viewer
│   │
│   ├── company_dashboard.html     # Company main dashboard
│   ├── company_details.html       # Company profile
│   ├── create_drive.html          # Drive creation form
│   │
│   ├── admin_dashboard.html       # Admin main dashboard
│   ├── admin_student_application.html  # Application management
│   ├── admin_drive_details.html   # Drive oversight
│   └── admin_student_application.html  # User management
│
├── static/                         # Static assets (CSS, images, JavaScript)
│
├── instance/                       # Flask instance folder (runtime data)
│   └── placement.db               # SQLite database file
│
└── __pycache__/                   # Python cache files (auto-generated)
```

---

## 🚀 How to Run

### Start the Flask Development Server
```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000/**

### Default Test Credentials
- **Admin**: Username: `admin` | Password: `admin123`

### Access Different Dashboards
- **Admin Dashboard**: Log in as Admin → `/admin`
- **Company Dashboard**: Log in as Company → `/company`
- **Student Dashboard**: Log in as Student → `/student`

---

## 🔑 Key Routes & Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/login` | GET, POST | User login |
| `/register` | GET, POST | User registration |
| `/logout` | GET | User logout |
| `/admin` | GET | Admin dashboard |
| `/company` | GET | Company dashboard |
| `/student` | GET | Student dashboard |
| `/approve_company/<username>` | GET | Admin approves company |
| `/blacklist/<username>` | GET | Admin blacklists user |
| `/admin/application/<app_id>` | GET | View application details |

---

## 🔒 Security Features

- **Session Management**: Flask session management for authenticated requests
- **Role-Based Access Control**: Different permissions for Admin, Company, and Student roles
- **Status Verification**: Account status checks (Approved, Pending, Blacklisted)
- **Password Storage**: Password-based authentication (consider hashing in production)
- **CSRF Protection**: Built-in Flask security mechanisms

---

## 🚧 Future Enhancements

- Password hashing and encryption (bcrypt/werkzeug)
- Email notifications for application status updates
- Advanced filtering and search functionality
- File upload for resumes and documents
- Payment gateway integration for premium features
- API endpoints for mobile app development
- Analytics and reporting dashboard
- Performance optimization and caching

---

## 📝 License

This project is developed for educational purposes as part of a placement management system initiative.

---

## 👨‍💼 Developer Notes

- The application uses Flask blueprints structure for maintainability
- SQLite is suitable for development; consider PostgreSQL for production deployment
- Implement proper error handling and validation in production
- Add comprehensive logging for debugging and monitoring
- Consider implementing database migrations using Alembic

---

## 💡 Support & Contribution

For issues, suggestions, or contributions, please reach out to the development team or submit a pull request to the repository.

---

**Last Updated**: March 2026
