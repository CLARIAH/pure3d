from flask import Flask, render_template
from functions import user_buttons, workflow, editionsList, projectsList, editions_page

app = Flask(__name__)
users_roles, projects = workflow()


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", user=user_buttons(), user_text="")


@app.route("/<username>")
def login(username):
    user_text = f"""
    {username} is logged in.
    """
    return render_template("index.html", user=user_buttons(), user_text=user_text)


@app.route("/projects")
def projects():
    projects_list = projectsList()
    return render_template(
        "projects.html", user=user_buttons(), projects_list=projects_list
    )


@app.route("/projects/<project_title>")
# Display for individual project
def project_page(project_title):
    projects_user, editions_list = editionsList(project_title)
    return render_template(
        "editions.html",
        user=user_buttons(),
        project_user=projects_user,
        editions_list=editions_list,
    )


@app.route("/projects/<project_title>/<edition_title>")
def edition_page(project_title, edition_title):
    edition_users = editions_page(project_title, edition_title)
    return render_template(
        "editionUsers.html", user=user_buttons(), edition_users=edition_users
    )


@app.route("/users")
def users():
    return render_template("users.html", user=user_buttons(), user_roles=users_roles)


if __name__ == "__main__":
    app.run(debug=True)
