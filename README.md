# MyTaskApp

Project Overview
This application is built using Python's Flask framework. It provides a platform for task management with role-based access control (RBAC), user authentication, and secure data handling.Security is emphasized in the application itself, from password hashing to input validation and CSRF protection using Google reCAPTCHA.

Installation Instructions
1. Clone the Repository
git clone <repository-url>
cd <repository-folder>
2. Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate   # On Windows
3. Install Dependencies
pip install -r requirements.txt
4. Run the Application
python app.py

Security Features
1. Password Hashing:
Ensures passwords are stored securely using werkzeug.security.
2. Input Validation:
Flask-WTF validates all form inputs to prevent invalid or malicious entries.
3. CSRF Protection:
Protects forms from unauthorized actions via CSRF tokens.
4. Role-Based Access Control (RBAC):
Separates functionality between Admin and User roles.
5. Google reCAPTCHA:
Prevents bots from accessing login forms.
6. Secure Sessions:
Sessions are securely signed to prevent tampering.

Usage
Login:
    Use the default admin credentials (username: admin, password: password) or register a new user.
Admin Tasks:
    Add, edit, and delete tasks.
    Register new users or admins.
User Tasks:
    Log in to view tasks.
