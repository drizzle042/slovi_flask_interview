from components import app, models

@app.route("/")
def home():
    me = models.User(first_name="Chukwujiobi", last_name="Chukwujiobi")
    me.email = "chukwujiobicanon@yahoo.com"
    me.templates_created = [
        "Purple Hibiscus",
        "Last Goodman"
    ]

    me.save()
    return """<div style="text-align: center; margin-top: 25%;">
                <h1>Welcome</h1>
                <p>You have been added to the database successfully</p>
                <a href="/register">Signup</a>
                </div>"""

@app.post("/register/")
def register():
    pass