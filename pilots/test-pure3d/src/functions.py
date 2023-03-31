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
    userRole = workflow_yaml.userRole
    status = workflow_yaml.status
    name = workflow_yaml.name

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

    projects = {}
    for project, project_data in userRole["project"].items():
        project_title = name["project"][project]["title"]
        project_role = list(project_data.keys())[0]
        # print(project_role)
        project_user = list(project_data.values())[0]
        # print(project_user)
        isVisible = status["project"]["values"][project]
        editions = {}
        for edition, edition_data in userRole["edition"][project].items():
            edition_title = name["edition"][project][edition]["title"]
            edition_user = list(edition_data.keys())[0]
            edition_role = list(edition_data.values())[0]
            isPublished = status["edition"]["values"][project][edition]
            editions[edition_title] = {
                "users": {"editionUser": edition_user,
                          "editionRole": edition_role},
                "isPublished": isPublished,
            }
        projects[project_title] = {
            "projectRole": project_role,
            "projectUser": project_user,
            "isVisible": isVisible,
            "editions": editions,
        }

        projects_list = []
        for title, info in projects.items():
            project_status = info["isVisible"]
            project_user = info["projectUser"]
            project_role = info["projectRole"]
            projects_list.append(
                    f"""
                    <a href= projects/{title}>{title}</a>
                    <br>
                    isVisible: {project_status}
                    <br>
                    <br>
                    """
                )
            editions = projects[title]["editions"]
            for editionTitles, editionInfo in editions.items():
                editions_list = []
                edition_status = editionInfo["isPublished"]
                edition_user = editionInfo["users"]["editionUser"]
                edition_role = editionInfo["users"]["editionRole"]
                editions_list.append(
                    f"""
                    Project Organisers - {project_user} : {project_role}
                    <br>
                    {editionTitles}
                    <br>
                    isPublished: {edition_status}
                    <br>
                    <br>
                    <br>
                    """
                )
            editions_list = "\n".join(editions_list)
        projects_list = "\n".join(projects_list)
    return users_list, projects_list, projects, editions_list
