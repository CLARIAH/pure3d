import os
import yaml
from generic import deepAttrDict
BASE = os.path.expanduser("~/github/clariah/pure3d/pilots/test-pure3d")
SRC = f"{BASE}/src"

users = ['user1', 'user2', 'user3', 'user4']


def user_buttons():

    html = []
    for user in users:
        html.append(
                f"""<a href = {user}>
                <button type="submit" class=cv_btn>{user}</button>
                </a>
                """
        )
    html = '\n'.join(html)
    return html


def yaml_parser(filename):
    with open(f"{filename}.yml", "r") as yml_file:
        parsed_yml_file = yaml.safe_load(yml_file)
    return deepAttrDict(parsed_yml_file)


def workflow():
    users_list = []
    projects_info = []
    filename = f"{SRC}/workflow/init"
    workflow_yaml = yaml_parser(filename)
    user = workflow_yaml.userRole
    status = workflow_yaml.status

    for userRoles, userValues in user.items():
        if userRoles == "site":
            for username, role in userValues.items():
                users_list.append(f"""
                {username}: {role}
                <br>""")
            users_list = "\n".join(users_list)

        if userRoles == "project": 
            for projectNo, projectRoles in userValues.items():
                for projectuser, projectRole in projectRoles.items():
                    projects_info.append(
                        f"""
                        Project {projectNo} - 
                        <br>
                        {projectuser} : {projectRole}
                        """
                    )
                projects_info = "\n".join(projects_info)

    return users_list, projects_info