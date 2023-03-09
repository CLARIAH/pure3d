from flask import Flask, render_template

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


def create_app():
    # create the flask app
    app = Flask(__name__)

    @app.route('/')
    def home():
        user = user_buttons()
        return render_template('app.html', user=user, user_text=" ")

    @app.route('/<userN>')
    def userMessage(userN):
        user = user_buttons()
        user_text = f"""
        <!-- {userN} logged in-->
        This is {userN}.
        """
        return render_template(
            'app.html',
            user=user,
            user_text=user_text)   
    return app


if __name__ == '__main__':
    create_app().run(debug=True)
