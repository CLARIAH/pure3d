from flask import (
    Flask,
    render_template,
    session,
    url_for,
    redirect,
    request,
    jsonify,
    make_response,
    send_from_directory,
)
from flask_session import Session
from src.users import user_buttons, user_roles
from src.workflow import editions_list, projects_list, editions_page
from src.variables import SRC
import yaml


app = Flask(__name__)
app.secret_key = b"1fd10cad570c541436d134d760429d5901edfc71522723ad4e75d2aa0215ef3"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "some_session_cookie_name"
Session(app)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        app.static_folder, "favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@app.route("/<username>/login")
def login(username):
    session["user"] = username
    user_text = f"""
            {username} is logged in.
            """
    session["user_text"] = user_text
    response = make_response(redirect(url_for("home")), 302)
    response.headers["X-Comment"] = f"{username} logged in"
    return response


@app.route("/logout")
def logout():
    session.pop("user")
    session.pop("user_text")
    response = make_response(redirect(url_for("home")), 302)
    response.headers["X-Comment"] = "user logged out"
    return response


@app.route("/")
@app.route("/home")
def home():
    user_text = session.get("user_text")
    username = session.get("user")
    return render_template(
        "index.html", user=user_buttons(), user_text=user_text, username=username
    )


@app.route("/projects")
def projects():
    user_text = session.get("user_text")
    username = session.get("user")
    all_projects = projects_list()
    return render_template(
        "projects.html",
        user=user_buttons(),
        all_projects=all_projects,
        user_text=user_text,
        username=username,
    )


@app.route("/projects/<project_title>")
# Display for individual project
def project_page(project_title):
    user_text = session.get("user_text")
    username = session.get("user")
    projects_user, all_editions = editions_list(project_title)

    return render_template(
        "editions.html",
        user=user_buttons(),
        project_user=projects_user,
        all_editions=all_editions,
        user_text=user_text,
        username=username,
    )


@app.route("/projects/<project_title>/<edition_title>")
def edition_page(project_title, edition_title):
    user_text = session.get("user_text")
    username = session.get("user")
    edition_users, edition_title = editions_page(project_title, edition_title)
    return render_template(
        "editionUsers.html",
        user=user_buttons(),
        edition_users=edition_users,
        edition_title=edition_title,
        user_text=user_text,
        username=username,
    )


@app.route("/users")
def users():
    user_text = session.get("user_text")
    username = session.get("user")
    users_html = user_roles()
    return render_template(
        "users.html",
        user=user_buttons(),
        user_text=user_text,
        username=username,
        user_role=users_html,
    )


# Define the Flask route for updating the user role
@app.route("/update_data_values", methods=["POST"])
def update_data_values():
    # Get the key and value from the POST request data
    key = request.form["key"]
    value = request.form["value"]
    update_type = request.form["type"]
    project = request.form["project"]

    if key is None or value is None or update_type is None or project is None:
        return make_response(jsonify(success=False, message="Missing required form data"), 400)

    filename = f"{SRC}/workflow/init.yml"
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

    if update_type == "user":
        # Update the data dictionary with the modified user roles dictionary
        if key not in data["userRole"]["site"]:
            return make_response(jsonify(success=False, message="Invalid user"), 404)
        elif value not in ["root", "admin", "guest", "user"]:
            return make_response(
                jsonify(success=False, message="Invalid user role"), 422
            )
        else:
            data["userRole"]["site"][key] = value
            with open(filename, "w") as f:
                yaml.dump(data, f)
            return jsonify(
                success=True, message=f"status of {key} has changed to {value}"
            )
    elif update_type == "project":
        if key not in data["name"]["project"]:
            return make_response(
                jsonify(success=False, message="Project not found"), 400
            )
        # Update the data dictionary with the modified project statuses dictionary
        else:
            data["status"]["project"]["values"][key] = value
            with open(filename, "w") as f:
                yaml.dump(data, f)
            return jsonify(
                success=True, message=f"project status of {key} is now {value}"
            )
    elif update_type == "edition":
        # Update the data dictionary with the modified edition statuses dictionary
        if key not in data["name"]["edition"][project]:
            return make_response(
                jsonify(success=False, message="Edition not found"), 400
            )
        # Update the data dictionary with the modified edition statuses dictionary
        else:
            data["status"]["edition"]["values"][project][key] = value
            with open(filename, "w") as f:
                yaml.dump(data, f)
            return jsonify(
                success=True, message=f"edition status of {key} is now {value}"
            )
    else:
        return jsonify(success=False, error="Invalid update type")


if __name__ == "__main__":
    app.run(debug=True)
