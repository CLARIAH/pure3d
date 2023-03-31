from flask import Flask, render_template
from functions import user_buttons, workflow

app = Flask(__name__)
users_roles, projects_list, projects, elist = workflow()


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
    return render_template(
        "projects.html", user=user_buttons(), projects_list=projects_list
    )


@app.route("/projects/<string:project_title>")
# Display for individual project
def project_page(project_title):
    return render_template(
        "editions.html", user=user_buttons(), editions_list=elist
    )


@app.route("/users")
def users():
    return render_template("users.html", user=user_buttons(), user_roles=users_roles)


if __name__ == "__main__":
    app.run(debug=True)
