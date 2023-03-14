from flask import Flask, render_template, url_for
from functions import user_buttons, getProjectsList, dcReaderJSON, PROJECT_DIR


def create_app():
    # create the flask app
    app = Flask(__name__)

    @app.route('/')
    def home():
        user = user_buttons()
        return render_template(
            'app.html',
            user=user,
            user_text=" ",
            projects_link=" ")

    @app.route('/<userN>')
    def userMessage(userN):
        user = user_buttons()
        user_text = f"""
        This is {userN}.
        """
        projects_link = url_for('user_projects', userN=userN)

        return render_template(
            'app.html',
            user=user,
            user_text=user_text,
            userN=userN,
            projects_link=projects_link,
            )

    @app.route('/<userN>/projects')
    def user_projects(userN):

        user = user_buttons()
        header = f"List of projects for {userN} are:"
        user_text = f"""
        This is {userN}.
        """
        projectsList = []

        projectNumbers = getProjectsList(userN)

        for i in projectNumbers:
            jsonDir = f"{PROJECT_DIR}/{userN}/{i}/meta"
            jsonField = "dc.title"
            title = dcReaderJSON(jsonDir, jsonField)
            projectsList.append(
                f"""
                <li>{title}</li>
                """
            )
        projectsList = '\n'.join(projectsList)

        return render_template(
            'projects.html',
            user=user,
            user_text=user_text,
            userN=userN,
            header=header,
            projectsList=projectsList
            )
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
