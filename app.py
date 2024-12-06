from flask import Flask, render_template, request, redirect, url_for, flash, session
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session management

@app.route("/")
def home():
    tasks = database.get_all_tasks()
    return render_template("view.html", tasks=tasks, user_role=session.get("role"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = database.get_user_by_username(username)
        if user and user[2] == password:  # Simple password check (hashing should be added)
            session["username"] = user[1]
            session["role"] = user[3]
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        flash("Invalid credentials!", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

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
