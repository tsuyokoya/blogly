"""Blogly application."""

from pydoc import render_doc
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from models import User, Post, Tag, PostTag
import os

app = Flask(__name__)

# Specify the database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"

# Default is True, turn off to prevent overhead
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Prints all SQL statements to terminal
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "something"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

### User View Functions ###


@app.route("/")
def show_home_page():
    """Redirects to users page"""
    newest_posts = Post.get_newest_posts()

    return render_template("/home.html", newest_posts=newest_posts)


@app.route("/users")
def show_users_page():
    """Shows list of all users"""

    users = User.query.order_by(User.last_name)
    return render_template("base.html", users=users)


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Shows user details"""

    user = User.query.get(user_id)
    return render_template("userdetails.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
def show_edit_page(user_id):
    """Shows edit page for user"""

    user = User.query.get(user_id)

    if request.method == "GET":
        return render_template("useredits.html", user=user)

    if request.method == "POST":
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        user.image_url = request.form.get("image_url")
        db.session.add(user)
        db.session.commit()
        return redirect("/")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes user"""

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/new", methods=["GET", "POST"])
def show_add_users_page():
    """Shows page to add a new user"""

    if request.method == "GET":
        return render_template("newuserform.html")

    if request.method == "POST":
        first = request.form.get("first_name")
        last = request.form.get("last_name")
        image = request.form.get("image_url")

        if not image:
            image = "https://m.media-amazon.com/images/I/51zLZbEVSTL._AC_SL1200_.jpg"

        new_user = User(first_name=first, last_name=last, image_url=image)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")


### Post View Functions ###


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def create_post(user_id):
    """Create new post"""

    if request.method == "GET":
        user = User.query.get(user_id)
        tags = Tag.get_all_tags()
        return render_template("postform.html", user=user, tags=tags)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        selected_tags = request.form.getlist("check")
        # loop through each selected tag, if any, and add to db
        if selected_tags:
            for name in selected_tags:
                tag_id = Tag.query.filter_by(name=name).first().id
                db.session.add(PostTag(post_id=new_post.id, tag_id=tag_id))

        db.session.commit()
        return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post contents"""

    post = Post.query.get(post_id)
    return render_template("post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    """Edit post"""

    post = Post.query.get(post_id)
    user = post.user
    tags = Tag.get_all_tags()

    if request.method == "GET":
        return render_template("postedits.html", post=post, user=user, tags=tags)

    if request.method == "POST":
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        selected_tags = request.form.getlist("check")

        # delete all tags for this post
        PostTag.query.filter_by(post_id=post_id).delete()

        # loop through each selected tag, if any, and add to db
        if selected_tags:
            for name in selected_tags:
                tag_id = Tag.query.filter_by(name=name).first().id
                db.session.add(PostTag(post_id=post_id, tag_id=tag_id))

        db.session.commit()
        return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get(post_id)
    user = post.user

    PostTag.query.filter_by(post_id=post_id).delete()
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f"/users/{user.id}")


### Tag View Functions ###


@app.route("/tags")
def show_tags():
    """List all tags"""
    tags = Tag.get_all_tags()
    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Show tag details"""
    tag = Tag.query.get(tag_id)
    return render_template("tagdetails.html", tag=tag)


@app.route("/tags/new", methods=["GET", "POST"])
def add_tag():
    """Show form to add new tag or add new tag"""
    if request.method == "GET":
        return render_template("tagform.html")

    if request.method == "POST":
        tag = request.form.get("tag")
        new_tag = Tag(name=tag)
        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    """Edit tag"""
    tag = Tag.query.get(tag_id)

    if request.method == "GET":
        return render_template("tagedits.html", tag=tag)

    if request.method == "POST":
        tag.name = request.form.get("name")
        db.session.commit()
        return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    PostTag.query.filter_by(tag_id=tag_id).delete()
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect("/tags")
