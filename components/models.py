from datetime import date
import mongoengine as dbengine

class User(dbengine.Document):
    meta = {'collection': 'user_collection'}
    first_name = dbengine.StringField(max_length=45)
    last_name = dbengine.StringField(max_length=45)
    email = dbengine.EmailField()
    password = dbengine.StringField()
    date_created = dbengine.DateTimeField(default=date.today())
    templates_created = dbengine.ListField()