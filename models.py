from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
  """Creates user model"""

  __tablename__ = "users"

  def __repr__(self):
    """Show info about user"""
    u = self
    return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}>"

  id = db.Column(db.Integer, primary_key = True,autoincrement = True)
  first_name = db.Column(db.String(50),nullable = False)
  last_name = db.Column(db.String(50),nullable = False)
  image_url = db.Column(db.Text)

  posts = db.relationship('Post', cascade = "all,delete-orphan", backref = 'user')

  def get_full_name(self):
    """Get full name of user"""
    return f"{self.first_name} {self.last_name}"


class Post(db.Model):
  """Creates post model"""

  __tablename__ = "posts"

  def __repr__(self):
    u = self
    return f"<Post id={u.id} title={u.title} content={u.content} created_at={u.created_at}>"

  id = db.Column(db.Integer, primary_key = True,autoincrement=True)
  title = db.Column(db.Text, nullable = False)
  content = db.Column(db.Text, nullable = False)
  created_at = db.Column(db.DateTime, server_default = db.func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

  post_tags = db.relationship('PostTag',cascade = "all,delete", backref = 'posts')

  @classmethod
  def get_newest_posts(cls):
    """Get the 5 newest post"""
    return cls.query.order_by(desc('created_at')).limit(5).all()

class Tag(db.Model):
  """Creates tag model"""

  __tablename__ = "tags"

  def __repr__(self):
    u = self
    return f"<Tag id={u.id} name={u.name}>"

  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  name = db.Column(db.String(50), nullable = False)

  post_tags = db.relationship('PostTag',cascade = "all,delete", backref = 'tags')
  posts = db.relationship('Post',secondary='post_tags',backref='tags')

  @classmethod
  def get_all_tags(cls):
    """Gets all tags"""
    return cls.query.all()

class PostTag(db.Model):
  """Creates model to identify tag to each post"""

  __tablename__ = "post_tags"

  def __repr__(self):
    u = self
    return f"<PostTag post_id={u.post_id} tag_id={u.tag_id}>"

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)
