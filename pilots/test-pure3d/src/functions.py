import yaml

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
    return parsed_yml_file
