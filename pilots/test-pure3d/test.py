import yaml
from src.generic import deepAttrDict


def yaml_parser(filename):
    with open(f"{filename}.yml", "r") as yml_file:
        parsed_yml_file = yaml.full_load(yml_file)
    return deepAttrDict(parsed_yml_file)


filename = "/home/sohinim/github/clariah/pure3d/pilots/test-pure3d/src/workflow/init"
workflow_yaml = yaml_parser(filename)
status = workflow_yaml.status
user = workflow_yaml.userRole
for key, statusInfo in status.items():
    field = statusInfo.field
    values = statusInfo.values

    for (outerName, outerValue) in values.items():
        if key == "project":
            print(
                f"""Project {outerName} Status - {field}: {outerValue}
            """
            )
        elif key == "edition":
            for (innerName, innerValue) in outerValue.items():
                print(
                    f"""
                {outerName} - {innerName}
                {field} : {innerValue}
                """
                )

for userRoles, userValues in user.items():
    if userRoles == "project":
            for project_No, projectRoles in userValues.items():
                for projectUser, projectRole in projectRoles.items():
                    project = dict(
                        projectId=project_No,
                        project_user=projectUser,
                        project_role=projectRole) 
                    print(project)

    if userRoles == "edition":
        #editions_info = []
        #id = {'id': '1'}

        for projectNos, editionValues in userValues.items():
            for editionNo, editionRoles in editionValues.items():
                project['editionId'] = editionNo
                #print(project)
