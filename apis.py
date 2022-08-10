from flask import Flask
from flask_mongoengine import MongoEngine
import mongoengine as ME
from mongoengine.errors import NotUniqueError
import jwt

app = Flask(__name__)
# Configuration with MongoEngine
app.config["MONGODB_SETTINGS"] = {
    "host": "mongodb+srv://Chukwujiobi:Keshadel1@cluster0.2cf9reh.mongodb.net/sloviDB?retryWrites=true&w=majority"
    }
mongo = MongoEngine(app)

app.config["SECRET_KEY"] = "26cfb735340e889d6ec3a08b5b07e5576ba47fb45eca0152cab9167936d0936c"


# DB models
class Templates(ME.EmbeddedDocument):
    template_name = ME.StringField(required=True)
    subject = ME.StringField()
    body = ME.StringField()

class User(ME.Document):
    first_name = ME.StringField()
    last_name = ME.StringField()
    email = ME.EmailField(required=True, unique=True)
    password = ME.StringField(required=True)
    template = ME.EmbeddedDocumentField(Templates)



@app.get("/register/")
def home():
    userData = {
                "first_name" : 'Andrew',
                "last_name" : 'Me',
                "email" : 'meetAndrew@subi.com',
                "password" : 'you are progressing!'
              }

    try:
        user_registrar = User()
        user_registrar.first_name = userData['first_name']
        user_registrar.last_name = userData['last_name']
        user_registrar.email = userData['email']
        user_registrar.password = userData['password']
        user_registrar.save()

        user = User.objects(email= userData["email"])
        
        access_token = jwt.encode(payload={"email": user[0]["email"], "password": user[0]["password"]}, key=app.config["SECRET_KEY"], algorithm="HS256")

        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">You have been registered successfully. This is your access token {access_token}</div>"""

        return response

    except NotUniqueError as e:
        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted red;color: red;">User already exists</div>"""

        return response

@app.get("/login/")
def login():
    credentials = {
                "email" : 'canon@subi.com',
                "password" : '112112112'
              }  
    try:
        user = User.objects(email= credentials["email"], password= credentials['password'])

        access_token = jwt.encode(payload={"email": user[0]["email"], "password": user[0]["password"]}, key=app.config["SECRET_KEY"], algorithm="HS256")

        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">You have been loggedin successfully \n Your access-token is {access_token}</div>"""

        return response

    except IndexError as e:
        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted red;color: red;">Could not log you in. Please check your email and password</div>"""

        return response

@app.get("/template/")
def create_template():
    template4 =  {
                    'template_name': 'We are the children',
                    'subject': 'Testing one',
                    'body': 'Hello World',
                }  
    template5 =  {
                    'template_name': 'We are the children',
                    'subject': 'Testing one',
                    'body': 'Hello World',
                }  
    template6 =  {
                    'template_name': 'We are the children',
                    'subject': 'Testing one',
                    'body': 'Hello World',
                }  

    return f"""<div></div>"""

@app.get("/template/")
def get_all_template():

    return f"""<div></div>"""


@app.get("/template/<template_id>")
def get_template(template_id):

    return f"""<div></div>"""


@app.get("/template/<template_id>")
def update_template(template_id):
    update = {
                    'template_name': 'We are the children',
                    'subject': 'Testing one',
                    'body': 'Hello World',
                }   
                
    return f"""<div></div>"""


@app.get("/template/<template_id>")
def delete_template(template_id):
    
    return f"""<div></div>"""


if __name__=="__main__":
    app.run(debug=True)