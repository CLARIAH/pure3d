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
            f"""<a href = "/{user}/login">
                <button type="submit">{user}</button>
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
        project_user = list(project_data.keys())[0]
        project_role = list(project_data.values())[0]
        isVisible = status["project"]["values"][project]
        editions = {}
        for edition, edition_data in userRole["edition"][project].items():
            edition_title = name["edition"][project][edition]["title"]
            users = {}
            for user, user_role in edition_data.items():
                users[user] = user_role
            isPublished = status["edition"]["values"][project][edition]
            editions[edition] = {
                "editionTitle": edition_title,
                "users": users,
                "isPublished": isPublished,
            }
        projects[project] = {
            "projectTitle": project_title,
            "projectRole": project_role,
            "projectUser": project_user,
            "isVisible": isVisible,
            "editions": editions,
        }

    return users_list, projects


def projectsList():
    a, projects = workflow()
    projects_list = []
    for projectID, info in projects.items():
        project_status = info["isVisible"]
        title = info["projectTitle"]
        projects_list.append(
            f"""
                    <a href= projects/{projectID}>{title}</a>
                    <br>
                    isVisible: {project_status}
                    <br>
                    <br>
                    """
        )
    projects_list = "\n".join(projects_list)
    return projects_list


def editionsList(project):
    a, projects = workflow()
    project_users = []
    project_role = projects[project]["projectRole"]
    project_user = projects[project]["projectUser"]
    project_title = projects[project]["projectTitle"]
    project_users.append(
        f"""
            <h1>{project_title}</h1>
            <br>
            <h2> Project Users </h2>
            {project_user} : {project_role}
            <br>
        """
    )
    project_users = "\n".join(project_users)

    editions = projects[project]["editions"]
    editions_list = []
    for editionID, editionInfo in editions.items():
        edition_status = editionInfo["isPublished"]
        edition_title = editionInfo["editionTitle"]
        editions_list.append(
            f"""

                <a href = /projects/{project}/{editionID}>
                {edition_title}
                </a>
                <br>
                isPublished: {edition_status}
                <br>
                <br>
            """
        )
    editions_list = "\n".join(editions_list)
    print(editions_list)
    return project_users, editions_list


def editions_page(project, edition):
    a, projects = workflow()
    editions = projects[project]["editions"][edition]
    edition_title = editions["editionTitle"]
    users = editions["users"]
    edition_users = []
    for user, role in users.items():
        edition_users.append(
            f"""
            {user} : {role}
            <br>
            """
        )
    edition_users = "\n".join(edition_users)
    print(edition_users)
    return edition_users, edition_title
