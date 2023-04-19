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
