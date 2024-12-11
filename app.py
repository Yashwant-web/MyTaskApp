from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from werkzeug.security import generate_password_hash, check_password_hash
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For session and Flask-WTF CSRF protection
# Configure reCAPTCHA
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdN25gqAAAAAKVU42RHVy-eJdzT79WR7D0_vyOW'  
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdN25gqAAAAAAzdGmhXn02Ij4RcdtF62zLnetHg'
app.config['RECAPTCHA_USE_SSL'] = False

# WTForms for Login and Registration
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    recaptcha = RecaptchaField()

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("user", "User"), ("admin", "Admin")])

@app.route("/")
def home():
    tasks = database.get_all_tasks()
    return render_template("view.html", tasks=tasks, user_role=session.get("role"))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = database.get_user_by_username(username)
        if user and check_password_hash(user[2], password):  # hashed password
            session["username"] = user[1]
            session["role"] = user[3]
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials!", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        role = form.role.data

        # only admins can register other admins
        if role == "admin" and session.get("role") != "admin":
            flash("Only admins can create admin accounts.", "danger")
            return redirect(url_for("register"))

        # username already exists check
        existing_user = database.get_user_by_username(username)
        if existing_user:
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for("register"))

        # user with a hashed password
        hashed_password = generate_password_hash(password)
        database.add_user(username, hashed_password, role)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/add", methods=["GET", "POST"])
def add():
    if session.get("role") != "admin":
        flash("Access denied: Admins only!", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        database.add_task(title, description)
        flash("Task added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update(task_id):
    if session.get("role") != "admin":
        flash("Access denied: Admins only!", "danger")
        return redirect(url_for("home"))

    task = database.get_task(task_id)
    if not task:
        flash("Task not found!", "danger")
        return redirect(url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        database.update_task(task_id, title, description)
        flash("Task updated successfully!", "success")
        return redirect(url_for("home"))
    return render_template("update.html", task=task)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    if session.get("role") != "admin":
        flash("Access denied: Admins only!", "danger")
        return redirect(url_for("home"))

    database.delete_task(task_id)
    flash("Task deleted successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)
