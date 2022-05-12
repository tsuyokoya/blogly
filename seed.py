"""Seed file to make sample data for users db."""

from models import User, Post, Tag, PostTag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
bilbo = User(first_name = "Bilbo", last_name = "Baggins", image_url="https://cdn.costumewall.com/wp-content/uploads/2018/10/bilbo-baggins.jpg")
saruman = User(first_name = "Saruman", last_name = "The White", image_url="https://wallpapercave.com/wp/wp2347888.jpg")
gandalf = User(first_name = "Gandalf", last_name = "The Grey", image_url="https://cdn.vox-cdn.com/thumbor/OkwKL3peHbhPz3S4Rq74CDgOK1c=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22323904/ian_mckellan_gandalf_4k_lotr.jpg")
frodo = User(first_name = "Frodo", last_name = "Baggins", image_url="https://i.pinimg.com/originals/98/f3/09/98f309bd89d9ed8fe2133589012aa089.jpg")


# Add new objects to session, so they'll persist
db.session.add(bilbo)
db.session.add(saruman)
db.session.add(gandalf)
db.session.add(frodo)

# Commit users
db.session.commit()

# Add posts & tags
objects = [
  Post(title="Wait", content = "Saruman you can't be serious. Fool.", user_id = "3"),
  Post(title="My Great Adventure", content = "I slayed a dragon", user_id = "1"),
  Post(title="Actually...", content = "I am NOT evil...Gandalf is.", user_id = "2"),
  Post(title="I Love Food", content = "Especially hot taters", user_id = "1"),
  Post(title="About Me", content = "I am so evil", user_id = "2"),
  Tag(name = "Evil"),
  Tag(name = "Adventure"),
  Tag(name = "Daring"),
  Tag(name = "Funny")
]

# Add new objects to session
db.session.bulk_save_objects(objects)

post_tag_one = PostTag(post_id=1, tag_id=4)
post_tag_two = PostTag(post_id=1, tag_id=3)
post_tag_three = PostTag(post_id=5, tag_id=1)
post_tag_four = PostTag(post_id=2, tag_id=2)

db.session.add(post_tag_one)
db.session.add(post_tag_two)
db.session.add(post_tag_three)
db.session.add(post_tag_four)

# Commit posts
db.session.commit()

