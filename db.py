from mongoengine import *

connect("cathive-1")


class Item(Document):
    title = StringField()
    url = StringField()
    content = StringField()
    added_epochtime = IntField()
    content_html = FileField()

    meta = {
        "indexes": [
            {
                "fields": ["$title", "$content", "$url"],
                "default_language": "english",
                "weights": {"title": 10, "content": 2, "url": 1},
            }
        ]
    }
