from flask import Flask, render_template
from functions import user_buttons, yaml_parser
import os

BASE = os.path.expanduser(
    "~/github/clariah/pure3d/pilots/test-pure3d")
SRC = f"{BASE}/src"

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        user=user_buttons(),
        user_text="")


@app.route('/<username>')
def login(username):
    user_text = f"""
    {username} is logged in.
    """
    return render_template(
        'index.html',
        user=user_buttons(),
        user_text=user_text)


@app.route('/projects')
def projects():
    projects_list = []
    yaml_filename = f"{SRC}/workflow/init"
    yaml_parsed = yaml_parser(yaml_filename)
    projects = dict(yaml_parsed["userRole"]["project"])

    for key, value in projects.items():
        dict_value = dict(value)
        projects_key = key

        for key, value in dict_value.items():
            projects_list.append(f"""
                Project {projects_key} :
                <br>
                {key} : {value}
                <br>
                editions available:
                <br>
                <br>
                """)
    projects_list = '\n'.join(projects_list)

    return render_template(
        'projects.html',
        user=user_buttons(),
        projects_list=projects_list)


@app.route('/users')
def users():
    user_roles_list = []
    yaml_filename = f"{SRC}/workflow/init"
    yaml_parsed = yaml_parser(yaml_filename)
    users_roles = dict(yaml_parsed["userRole"]["site"])

    for key, value in users_roles.items():
        user_roles_list.append(f"""
        {key} : {value}
        <br>
        """)
    user_roles_list = '\n'.join(user_roles_list)
    
    return render_template(
        'users.html',
        user=user_buttons(),
        user_roles=user_roles_list)


if __name__ == '__main__':
    app.run(debug=True)
