from flask import Flask, request
from flask_mongoengine import MongoEngine
import mongoengine as ME
import json
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
    template = ME.EmbeddedDocumentListField(Templates)


@app.get("/")
def home():
    return """<div style="text-align: center; padding: 200px; color: gray; border: 1px dotted green;">Welcome To Slovi Interview Api Staging</div>"""

@app.post("/register/")
def register():
    userData = request.json

    try:
        user_registrar = User()
        user_registrar.first_name = userData['first_name']
        user_registrar.last_name = userData['last_name']
        user_registrar.email = userData['email']
        user_registrar.password = userData['password']
        user_registrar.template = []
        user_registrar.save()

        user = User.objects(email__iexact= userData["email"])
        
        access_token = jwt.encode(payload={"email": user[0]["email"], "password": user[0]["password"]}, key=app.config["SECRET_KEY"], algorithm="HS256")

        response = {"accessToken": access_token}

        return response

    except NotUniqueError as e:
        response = {"message": "User already exists. Instead login"}

        return response

@app.post("/login/")
def login():
    credentials = request.json
    try:
        user = User.objects(email__iexact= credentials["email"], password__exact= credentials['password'])

        access_token = jwt.encode(payload={"email": user[0]["email"], "password": user[0]["password"]}, key=app.config["SECRET_KEY"], algorithm="HS256")

        response = {"accessToken": access_token}

        return response

    except IndexError as e:
        response = {"message": "Could not log you in. Please check your email and password"}

        return response

@app.post("/template/")
def create_template():
    templateData =  request.json

    user_access_token = request.headers.get("Authorization").split()[1]

    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])

    template = Templates(
        template_name = templateData["template_name"],
        subject = templateData["subject"],
        body = templateData["body"]
    )

    userTemplateAdd = User.objects(email__iexact= access_token_decoded["email"]).first()
    userTemplateAdd["template"].append(template)
    userTemplateAdd.save()

    response = {"message": "Template was added successfully"}

    return response

@app.get("/template")
def get_all_template():
    
    user_access_token = request.headers.get("Authorization").split()[1]

    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])

    user_json = User.objects(email__iexact= access_token_decoded["email"])[0].to_json()
    user_templates = json.loads(user_json)["template"]

    response = {"data": user_templates}

    return response


@app.get("/template/<template_id>")
def get_template(template_id):
    
    user_access_token = request.headers.get("Authorization").split()[1]
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    user_json = User.objects(email__iexact= access_token_decoded["email"])[0].to_json()
    user_template = json.loads(user_json)["template"][int(template_id) - 1]
    
    response = {"data": user_template}
    
    return response


@app.put("/template/<template_id>")
def update_template(template_id):
    update = request.json
    
    user_access_token = request.headers.get("Authorization").split()[1]
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    template_to_update = User.objects(email__iexact= access_token_decoded["email"]).first()
    template_updated = template_to_update["template"][int(template_id) - 1]
    template_updated["template_name"] = update["template_name"]
    template_updated["subject"] = update["subject"]
    template_updated["body"] = update["body"]
    template_to_update.save()

    template_json = json.loads(template_to_update.to_json())["template"]
    
    response = {"message": "The template has been updated successfully", "data": template_json}

    return response


@app.delete("/template/<template_id>")
def delete_template(template_id):

    user_access_token = request.headers.get("Authorization").split()[1]
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    template_to_delete = User.objects(email__iexact= access_token_decoded["email"]).first()
    del template_to_delete["template"][int(template_id) - 1]
    template_to_delete.save()
    
    response = {"message": "The template has been deleted successfully"}
    
    return response


if __name__=="__main__":
    app.run(debug=False)