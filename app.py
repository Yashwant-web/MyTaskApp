from flask import Flask, render_template, request, redirect, url_for, flash
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

@app.route("/")
def home():
    tasks = database.get_all_tasks()
    return render_template("view.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        database.add_task(title, description)
        flash("Task added successfully!", "success")
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/update/<int:task_id>", methods=["GET", "POST"])
def update(task_id):
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
    database.delete_task(task_id)
    flash("Task deleted successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)
