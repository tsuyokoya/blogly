from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests views for User"""

    def setUp(self):
        """Add sample user and post"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Mrs.", last_name="Tester")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='hello', content='yo', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_page(self):
        """Test home page"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertIn('Blogly Recent Posts', html)
            self.assertIn('Mrs. Tester', html)
            self.assertIn('hello', html)
            self.assertEqual(resp.status_code, 200)

    def test_users_list(self):
        """Test user listed on users page"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Tester, Mrs.', html)
            self.assertIn('All Users', html)

    def test_show_users(self):
        """Test display of user details page"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Mrs. Tester\'s Bio', html)
            self.assertIn('hello', html)

    def test_create_user(self):
        """Test addition of new user"""
        with app.test_client() as client:
            new_user = {"first_name": "New", "last_name": "Tester"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Tester, New", html)

    def test_edit_user(self):
        """Test edit of existing user"""
        with app.test_client() as client:
            updated_user = {"first_name": "Updated", "last_name": "Tester"}
            resp = client.post(f"/users/{self.user_id}/edit", data=updated_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Updated Tester", html)

    def test_delete_user(self):
        """Test deletion of existing user"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Tester, Mrs.', html)

class PostViewsTestCase(TestCase):
    """Test views for posts"""

    def setUp(self):
        """Add sample user and post"""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="Mrs.", last_name="Tester")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='hello', content='yo', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_create_post(self):
        """Test post creation"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add New Post for',html)

            new_post = {"title": "Test2", "content": "Another Post"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=new_post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test2',html)
            self.assertNotIn('Add New Post for',html)

    def test_show_post(self):
        """Test post content display"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('hello', html)
            self.assertIn('yo', html)

    def test_edit_post(self):
        """Test post edit"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit', html)

            updated_post = {"title":"Updated!","content":"not much to say"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=updated_post, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Updated!',html)
            self.assertIn('not much to say',html)

    def test_delete_post(self):
        """Test post deletion"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/delete",follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('hello', html)

class TagsViewsTestCase(TestCase):
    """Test views for tags"""

    def setUp(self):
        """Add sample user, post, and tag"""
        Post.query.delete()
        Tag.query.delete()
        User.query.delete()

        user = User(first_name="Mrs.", last_name="Tester")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title='hello', content='yo', user_id=self.user_id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

        tag_one = Tag(name = 'introduction')
        tag_two = Tag(name = 'random')
        db.session.add(tag_one)
        db.session.add(tag_two)
        db.session.commit()

        self.tag_one_id = tag_one.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('introduction', html)
            self.assertIn('random', html)

    def test_create_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add a New Tag', html)

            new_tag = {"tag":"newtag"}
            resp = client.post(f"/tags/new", data = new_tag, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('newtag', html)

    def test_edit_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_one_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit', html)

            edit_tag = {"name":"edittag"}
            resp = client.post(f"/tags/{self.tag_one_id}/edit", data = edit_tag, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('edittag', html)

    def test_delete_tags(self):
        with app.test_client() as client:
            resp = client.post(f"/tags/{self.tag_one_id}/delete", follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('introduction', html)
            self.assertIn('random', html)