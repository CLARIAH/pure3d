from flask import Flask, render_template, session, url_for, redirect
from flask_session import Session
from user_login import user_buttons
from functions import workflow, editions_list, projects_list, editions_page

app = Flask(__name__)
app.secret_key = b"1fd10cad570c541436d134d760429d5901edfc71522723ad4e75d2aa0215ef3"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/<username>/login")
def login(username):
    session["user"] = username
    user_text = f"""
            {username} is logged in.
            """
    session["user_text"] = user_text
    return redirect(url_for("home"))


@app.route("/")
@app.route("/home")
def home():
    user_text = session.get("user_text")
    return render_template("index.html", user=user_buttons(), user_text=user_text)


@app.route("/projects")
def projects():
    user_text = session.get("user_text")
    all_projects = projects_list()
    return render_template(
        "projects.html",
        user=user_buttons(),
        all_projects=all_projects,
        user_text=user_text,
    )


@app.route("/projects/<project_title>")
# Display for individual project
def project_page(project_title):
    user_text = session.get("user_text")
    projects_user, all_editions = editions_list(project_title)

    return render_template(
        "editions.html",
        user=user_buttons(),
        project_user=projects_user,
        all_editions=all_editions,
        user_text=user_text,
    )


@app.route("/projects/<project_title>/<edition_title>")
def edition_page(project_title, edition_title):
    user_text = session.get("user_text")
    edition_users, edition_title = editions_page(project_title, edition_title)
    return render_template(
        "editionUsers.html",
        user=user_buttons(),
        edition_users=edition_users,
        edition_title=edition_title,
        user_text=user_text,
    )


@app.route("/users")
def users():
    user_text = session.get("user_text")
    users_roles, projects = workflow()
    return render_template(
        "users.html", user=user_buttons(), user_roles=users_roles, user_text=user_text
    )


if __name__ == "__main__":
    app.run(debug=True)
