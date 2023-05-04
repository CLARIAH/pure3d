from functions import yaml_parser
from variables import SRC


def workflow():
    filename = f"{SRC}/workflow/init"
    workflow_yaml = yaml_parser(filename)
    userRole = workflow_yaml.userRole
    status = workflow_yaml.status
    name = workflow_yaml.name

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

    return projects


def projects_list():
    projects = workflow()
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


def editions_list(project):
    projects = workflow()
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
    return project_users, editions_list


def editions_page(project, edition):
    projects = workflow()
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
    return edition_users, edition_title
