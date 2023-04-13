from flask import Flask, render_template, session, url_for, redirect
from functions import user_buttons, workflow, editionsList, projectsList, editions_page

app = Flask(__name__)
users_roles, projects = workflow()

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'


@app.route("/home")
def home():
    return render_template("index.html", user=user_buttons(), user_text="")


@app.route("/<username>")
def login(username):
    user_text = f"""
    {username} is logged in.
    """
    return render_template("index.html", user=user_buttons(), user_text=user_text)


@app.route("/<username>/login")
def logging(username):
    session['username'] = f"{username}"
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


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
