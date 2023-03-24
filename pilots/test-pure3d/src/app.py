from flask import Flask, render_template
from functions import user_buttons, workflow

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", user=user_buttons(), user_text="")


@app.route("/<username>")
def login(username):
    user_text = f"""
    {username} is logged in.
    """
    return render_template(
        "index.html",
        user=user_buttons(),
        user_text=user_text)


@app.route("/projects")
def projects():

    users_roles, projectsRoles = workflow()

    #projects_list = []
    #yaml_parsed = yaml_parseraml_filename)
    
    #editions_list = []
    #ep = {}
    #editions = dict(yaml_parsed["userRole"]["edition"])
    #for p in projects_key:
        #ep = editions[p]
        #for ed_key, ed_value in ep.items():
            #for ed_key in projects_key:
                #for ed_value_key, ed_value_value in dict(ed_value).items():
                    #for ed_value_value_key, ed_value_value_value in dict(
                       # ed_value_value
                    #).items():
                        #editions_list.append(
                            #f"""
                        #Edition {ed_value}
                        #<br>
                        #{ed_value_key}: {ed_value_value}
                        #"""
                        #)
    #editions_list = "\n".join(editions_list)

    return render_template(
        "projects.html",
        user=user_buttons(),
        projects_list=projectsRoles,
        #editions_list=editions_list,
    )


@app.route("/users")
def users():
    users_roles, projectsRoles = workflow()

    return render_template(
        "users.html", user=user_buttons(),
        user_roles=users_roles
    )


if __name__ == "__main__":
    app.run(debug=True)
