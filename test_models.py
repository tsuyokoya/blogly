from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests User model method"""

    def test_get_full_name(self):
        user = User(first_name="Mr.", last_name="Test")
        self.assertEqual(user.get_full_name(), "Mr. Test")

class PostModelTestCase(TestCase):
    """Tests User model"""

    def setUp(self):
        """Clean up any existing users. Create test user and posts"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name = "Test", last_name = "Case")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        posts = [
            Post(title="Wait", content = "Saruman you can't be serious. Fool.", user_id = self.user_id),
            Post(title="My Great Adventure", content = "I slayed a dragon", user_id = self.user_id),
            Post(title="Actually...", content = "I am NOT evil...Gandalf is.", user_id = self.user_id),
            Post(title="I Love Food", content = "Especially hot taters", user_id = self.user_id),
            Post(title="About Me", content = "I am so evil", user_id = self.user_id),
            Post(title="This is", content = "such a fun time", user_id = self.user_id)
        ]

        db.session.bulk_save_objects(posts)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_get_newest_posts(self):
        """Test if class method returns 5 most recent posts"""
        newest_posts = Post.get_newest_posts()

        self.assertEqual(len(newest_posts), 5)
        self.assertNotIn(Post.query.all()[5], newest_posts)

class PostModelTestCase(TestCase):
    """Tests User model"""

    def setUp(self):
        """Clean up any existing users. Create test tags"""

        Tag.query.delete()

        tags = [
            Tag(name = "one"),
            Tag(name = "two"),
            Tag(name = "three")
        ]

        db.session.bulk_save_objects(tags)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_get_all_tags(self):
        """Test if class method returns all test tags"""
        all_tags = Tag.get_all_tags()

        self.assertEqual(len(all_tags), 3)
        self.assertIn(Tag.query.all()[0], all_tags)
        self.assertIn(Tag.query.all()[1], all_tags)
        self.assertIn(Tag.query.all()[2], all_tags)
