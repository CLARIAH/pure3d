from flask import Flask, render_template

users = ['user1', 'user2', 'user3','user4']

# create the flask app
app = Flask(__name__)

@app.route('/')
def home():
    html = []
    for user in users:
        html.append(
            f"""<a href = {user}> <button type="submit" class=cv_btn>{user}</button> </a> """
        )
    html = '\n'.join(html) 
    return render_template('app.html', user=html, user_text =" ")
    
@app.route('/<userN>')
def userMessage(userN):
    user_text = f"This is {userN}"
    return render_template('app.html', user = " ", user_text=user_text )


# boilerplate flask app code
if __name__ == "__main__":
    app.run(debug=True)
