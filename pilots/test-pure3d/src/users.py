from functions import yaml_parser
from variables import SRC

filename = f"{SRC}/workflow/init"
workflow_yaml = yaml_parser(filename)
userRole = workflow_yaml.userRole


def user_buttons():
    for userRoles, userValues in userRole.items():
        if userRoles == "site":
            users = []
            for username, role in userValues.items():
                users.append(
                    f"""
                    <a href = "/{username}/login">
                    <button type="submit">{username}</button>
                    </a>
                    """
                )
            users = "\n".join(users)
    return users


def user_roles():
    options = ["root", "admin", "guest", "user"]

    for userRoles, userValues in userRole.items():
        if userRoles == "site":
            html = []

            for key, value in userValues.items():
                select_options = ""
                for option in options:
                    selected = "selected" if value == option else ""
                    select_options += (
                        f"<option value='{option}' {selected}>{option}</option>"
                    )

                html.append(
                    f"""
                    <tr>
                        <td>{key}</td>
                        <td id="{key}">
                            <span class="value">{value}</span>
                            <select id='select-{key}' onchange='changeDataValues("{key}", this.value, "user", " ")'>
                                {select_options}
                            </select>
                        </td>
                    </tr>
                    """
                )
            html = "\n".join(html)

    return html
