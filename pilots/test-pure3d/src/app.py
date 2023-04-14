from flask import Flask, render_template, session, url_for, redirect
from flask_session import Session
from functions import user_buttons, workflow, editionsList, projectsList, editions_page

app = Flask(__name__)
app.secret_key = b"1fd10cad570c541436d134d760429d5901edfc71522723ad4e75d2aa0215ef3"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users_roles, projects = workflow()


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
    return render_template("index.html",
                           user=user_buttons(),
                           user_text=user_text)


@app.route("/projects")
def projects():
    user_text = session.get("user_text")
    projects_list = projectsList()
    return render_template(
        "projects.html",
        user=user_buttons(),
        projects_list=projects_list,
        user_text=user_text,
    )


@app.route("/projects/<project_title>")
# Display for individual project
def project_page(project_title):
    user_text = session.get("user_text")
    projects_user, editions_list = editionsList(project_title)

    return render_template(
        "editions.html",
        user=user_buttons(),
        project_user=projects_user,
        editions_list=editions_list,
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
    return render_template(
        "users.html",
        user=user_buttons(),
        user_roles=users_roles,
        user_text=user_text
    )


if __name__ == "__main__":
    app.run(debug=True)
