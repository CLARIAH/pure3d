import os
import yaml
from generic import deepAttrDict

BASE = os.path.expanduser("~/github/clariah/pure3d/pilots/test-pure3d")
SRC = f"{BASE}/src"

users = ["user1", "user2", "user3", "user4"]


def user_buttons():

    html = []
    for user in users:
        html.append(
            f"""<a href = {user}>
                <button type="submit" class=cv_btn>{user}</button>
                </a>
                """
        )
    html = "\n".join(html)
    return html


def yaml_parser(filename):
    with open(f"{filename}.yml", "r") as yml_file:
        parsed_yml_file = yaml.safe_load(yml_file)
    return deepAttrDict(parsed_yml_file)


def workflow():
    filename = f"{SRC}/workflow/init"
    workflow_yaml = yaml_parser(filename)
    userRole = workflow_yaml["userRole"]
    project_status = workflow_yaml["status"]["project"]
    edition_status = workflow_yaml["status"]["edition"]
    projects_page = {}

    for userRoles, userValues in userRole.items():
        if userRoles == "site":
            users_list = []
            for username, role in userValues.items():
                users_list.append(
                    f"""
                {username}: {role}
                <br>"""
                )
            users_list = "\n".join(users_list)

    for project_id, project_data in userRole["project"].items():
        project_role = list(project_data.keys())[0]
        project_user = list(project_data.values())[0]
        isVisible = project_status["values"][project_id]
        editions = {}
        for edition_id, edition_data in userRole["edition"][project_id].items():
            users = {}
            for edition_user, edition_role in edition_data.items():
                users = dict(editionUser=edition_user,
                             editionRole=edition_role)
            isPublished = edition_status["values"][project_id][edition_id]
            editions[edition_id] = {"users": users, "isPublished": isPublished}
        projects_page[project_id] = {
            "projectRole": project_role,
            "projectUser": project_user,
            "isVisible": isVisible,
            "editions": editions,
        }

    projects_html = []
    for projectNames, projectInfos in projects_page.items():
        projects_html.append(
                f"""
                    Project {projectNames}
                    <br>
                    """
            )
    projects_html = "\n".join(projects_html)
    return users_list, projects_html
