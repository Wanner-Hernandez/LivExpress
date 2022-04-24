from enum import auto
from . import post
from liveexpress import db
from liveexpress.models import Post, User
from liveexpress.blog.forms import PostForm, SearchForm
from liveexpress.blog.utils.filters import filter_hashtags
from flask_login import current_user
from sqlalchemy import text
from flask import abort, render_template, request, jsonify, current_app, redirect, url_for, flash
import os
import secrets
from PIL import Image

def evalify(string):
    html = []
    try:
        if string is not None:
            listify = eval(string)

            for hashtag in listify:
                html.append(hashtag)
            return html
        else:
            return ["No Tags"]
    except:
        return ["No Tags"]

@post.route('/search', methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        title = form.title.data
        hashtag = form.hashtags.data
        if not title and not hashtag:
            # That mean all search inputs are empty
            return redirect(url_for("main.feed"))

        if title:
            query = f"SELECT * FROM post where title like '%{title}%'"
            posts = db.session.query(Post).from_statement(text(query)).all()
            
            # return str(posts)
            return render_template("filter_res.html", posts=posts, evalify=evalify)
        if hashtag:
            query = f"SELECT * FROM post where hashtags like '%{hashtag}%'"
            posts = db.session.query(Post).from_statement(text(query)).all()
            return render_template("filter_res.html", posts=posts, evalify=evalify)
            
    return render_template("search.html", form=form)


@post.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if post.author != current_user:
    # abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.feed'))


@post.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if post.author != current_user:
    #     abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@post.route("/create_post", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():

        hashtag_list = None
        hashtages = request.form.get("hidden-values")
        if hashtages:
            if hashtag_list is None:
                splitted = hashtages.split(",")
                hashtag_list = filter_hashtags(splitted)

        title = form.title.data
        content = form.content.data
        # return str(content)
        if form.image.data:
            try:
                picture_file = save_picture(form.image.data, (1300, 800))

            except:
                return render_template("errors/504.html")

            if current_user.is_authenticated:
                post = Post(title=title, content=content, hashtags=str(
                    hashtag_list), image_file=picture_file, author=current_user)
                db.session.add(post)
                db.session.commit()

                flash("Post Created successfully", "success")
                return redirect(url_for("main.feed"))
            else:
                guest = User.query.filter_by(username='guest').first()
                post = Post(title=title, content=content, hashtags=str(
                    hashtag_list), image_file=picture_file, author=guest)

                db.session.add(post)
                db.session.commit()
                flash("Post Created successfully", "success")
                return redirect(url_for("main.index"))
            return "Done"
    return render_template("create_post.html", form=form, title="Create Post")


@post.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)




def save_picture(form_picture, output_res):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/blog_pics', picture_fn)

    output_size = output_res
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
