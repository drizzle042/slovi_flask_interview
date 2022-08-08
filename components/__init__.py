from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
# This is a dev secret key. A more secure one will be created during production.
app.config['SECRET_KEY'] = "bf35500ed0700d344730d78614d11be97bd1e616"
app.config['MONGO_URI'] = 'mongodb+srv://Canon:Keshadel1@slovi-interview-test.89rmoe0.mongodb.net/?retryWrites=true&w=majority'

# Mongodb setup
client = PyMongo(app)
db = client.db

from components import views