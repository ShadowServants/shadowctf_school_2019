from app import db


class User(db.Document):
    login = db.StringField(max_length=255)
    password = db.StringField(max_length=255)


class WebPage(db.Document):
    url = db.StringField(max_length=512)
    content = db.StringField()
    user_id = db.StringField()

    meta = {'indexes': [
        {'fields': ["$content"],
         'weights': {'content': 20}
         }
    ]}

