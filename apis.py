from flask import Flask
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



@app.get("/register/")
def home():
    userData = {
                "first_name" : 'Canon',
                "last_name" : 'Me',
                "email" : 'canon@subi.com',
                "password" : 'hello world!'
              }

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

        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">You have been registered successfully. This is your access token \n {access_token}</div>"""

        return response

    except NotUniqueError as e:
        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted red;color: red;">User already exists</div>"""

        return response

@app.get("/login/")
def login():
    credentials = {
                "email" : "andrewgarfield@subi.com",
                "password" : 'hello world!'
              }  
    try:
        user = User.objects(email__iexact= credentials["email"], password__exact= credentials['password'])

        access_token = jwt.encode(payload={"email": user[0]["email"], "password": user[0]["password"]}, key=app.config["SECRET_KEY"], algorithm="HS256")

        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">You have been loggedin successfully. <br>Your access-token is <br><h1 style="text-align: center;">{access_token}</h1></div>"""

        return response

    except IndexError as e:
        response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted red;color: red;">Could not log you in. Please check your email and password</div>"""

        return response

@app.get("/template/")
def create_template():
    templateData =  {
                    'template_name': 'Check this out',
                    'subject': 'It will work',
                    'body': "Hello World, I'm back again",
                }

    user_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFuZHJld2dhcmZpZWxkQHN1YmkuY29tIiwicGFzc3dvcmQiOiJoZWxsbyB3b3JsZCEifQ.zdmCaX1IYzk2VNIJeB5ysM_feOqfaC42qWGLUfSozlQ"

    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])

    template = Templates(
        template_name = templateData["template_name"],
        subject = templateData["subject"],
        body = templateData["body"]
    )

    userTemplateAdd = User.objects(email__iexact= access_token_decoded["email"]).first()
    userTemplateAdd["template"].append(template)
    userTemplateAdd.save()

    response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">Template was created successfully</div>"""

    return response

@app.get("/template/get")
def get_all_template():
    
    user_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFuZHJld2dhcmZpZWxkQHN1YmkuY29tIiwicGFzc3dvcmQiOiJoZWxsbyB3b3JsZCEifQ.zdmCaX1IYzk2VNIJeB5ysM_feOqfaC42qWGLUfSozlQ"

    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])

    user_json = User.objects(email__iexact= access_token_decoded["email"])[0].to_json()
    user_templates = json.loads(user_json)["template"]

    response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">{json.dumps(user_templates)}</div>"""

    return response


@app.get("/template/<template_id>")
def get_template(template_id):
    
    user_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFuZHJld2dhcmZpZWxkQHN1YmkuY29tIiwicGFzc3dvcmQiOiJoZWxsbyB3b3JsZCEifQ.zdmCaX1IYzk2VNIJeB5ysM_feOqfaC42qWGLUfSozlQ"
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    user_json = User.objects(email__iexact= access_token_decoded["email"])[0].to_json()
    user_template = json.loads(user_json)["template"][int(template_id)]
    
    response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">{json.dumps(user_template)}</div>"""
    
    return response


@app.get("/template/update/<template_id>")
def update_template(template_id):
    update = {
                    'template_name': 'All with GOD',
                    'subject': 'Marvel',
                    'body': 'GOD Almighty',
                }   
    
    user_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNhbm9uQHN1YmkuY29tIiwicGFzc3dvcmQiOiJoZWxsbyB3b3JsZCEifQ.U314zp2qaGe-fE5BJTan33fSAoKX39k9GKsTlUwOxmw"
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    template_to_update = User.objects(email__iexact= access_token_decoded["email"]).first()
    template_updated = template_to_update["template"][int(template_id)]
    template_updated["template_name"] = update["template_name"]
    template_updated["subject"] = update["subject"]
    template_updated["body"] = update["body"]
    template_to_update.save()

    template_json = json.loads(template_to_update.to_json())["template"]
    
    response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">The template has been updated successfully <br>   {json.dumps(template_json)}</div>"""

    return response


@app.get("/template/delete/<template_id>")
def delete_template(template_id):

    user_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFuZHJld2dhcmZpZWxkQHN1YmkuY29tIiwicGFzc3dvcmQiOiJoZWxsbyB3b3JsZCEifQ.zdmCaX1IYzk2VNIJeB5ysM_feOqfaC42qWGLUfSozlQ"
    
    access_token_decoded = jwt.decode(user_access_token, key=app.config["SECRET_KEY"], algorithms=["HS256"])
    
    template_to_delete = User.objects(email__iexact= access_token_decoded["email"]).first()
    del template_to_delete["template"][int(template_id)]
    template_to_delete.save()
    
    template_json = json.loads(template_to_delete.to_json())["template"]
    
    response = f"""<div style="text-align: center; padding: 200px; margin: 20px; border: 1px dotted green; color: green;">The template has been deleted successfully</div>"""
    
    return response


if __name__=="__main__":
    app.run(debug=True)