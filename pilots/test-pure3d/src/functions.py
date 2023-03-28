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
    user = workflow_yaml.userRole
    status = workflow_yaml.status

    for userRoles, userValues in user.items():
        if userRoles == "site":
            users_list = []
            for username, role in userValues.items():
                users_list.append(
                    f"""
                {username}: {role}
                <br>"""
                )
            users_list = "\n".join(users_list)

        if userRoles == "project":
            projects_info = []
            for project_No, projectRoles in userValues.items():
                for projectUser, projectRole in projectRoles.items():
                    projects_info.append(
                            f"""
                        Project {project_No}
                        <br>
                        {projectUser} : {projectRole}
                        <br>
                        """
                    )
            projects_info = "\n".join(projects_info)         

        elif userRoles == "edition":

            editions = []
            for projectNos, editionValues in userValues.items():

                for editionNo, editionRoles in editionValues.items():
                    editions.append(f"""
                                        <br> Project {projectNos}
                                        Edition {editionNo}: {editionRoles}
                                        <br>
                                        """
                                    )
            editions = "\n".join(editions)

    for statusKey, statusValues in status.items():
        field = statusValues.field
        values = statusValues.values
        
        for projectStatusKeys, projectStatusValues in values.items():
            if statusKey == "project":
                projectStatus = []
                projectStatus.append(
                    f""" <br>
                    Project {projectStatusKeys} Status {field}: {projectStatusValues} 
                    """
                    )
                projectStatus = "\n".join(projectStatus)
                #print(projectStatus)

            elif statusKey == "edition":
                editionStatus = []
                for editionStatusKeys, editionStatusValues in projectStatusValues.items():
                    editionStatus.append(f"""
                    <br>
                                        Project {projectStatusKeys} -
                                        Edition {editionStatusKeys}
                                        {field} : {editionStatusValues}
                                        <br>
                                        """
                                         )
                editionStatus = "\n".join(editionStatus)
                #print(editionStatus)
    return users_list, projects_info, editions, projectStatus, editionStatus
