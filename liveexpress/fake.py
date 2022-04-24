""" Generates Dummy fake for Database """
from faker import Faker
from . import db
from .models import Post, User

fake = Faker() # Faker instance

class PostFakeData(object):
    def __init__(self, data_count=4):
        self.data_count = data_count

    def __call__(self):
        guest = User.query.filter_by(username="guest").first()
        for count in range(self.data_count):
            title = fake.paragraph(nb_sentences=1)
            content = fake.text()
            tags = str([fake.color_name() for i in range(2)])
            p = Post(title=title, content=content, hashtags=tags, author=guest)
            print(f"Adding Fake Post {title} to the db")
            db.session.add(p)
        db.session.commit()     
                        

