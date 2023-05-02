from functions import yaml_parser, SRC

filename = f"{SRC}/workflow/init"
workflow_yaml = yaml_parser(filename)
userRole = workflow_yaml.userRole


def user_buttons():
    for userRoles, userValues in userRole.items():
        if userRoles == "site":
            users = []
            for username, role in userValues.items():
                users.append(
                    f"""<a href = "/{username}/login">
                <button type="submit">{username}</button>
                </a>
                """
                )
            users = "\n".join(users)
    return users
