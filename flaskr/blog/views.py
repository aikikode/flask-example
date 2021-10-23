from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.auth.views import login_required
from flaskr.models import Post

blueprint = Blueprint('blog', __name__)


@blueprint.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc())
    return render_template('blog/index.html', posts=posts)


@blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.session.add(Post(title=title, body=body, author_id=g.user.id))
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(post_id, check_author=True):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    if check_author and post.author_id != g.user.id:
        abort(403)
    return post


@blueprint.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = get_post(post_id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))
        flash('Title is required.')

    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    db.session.delete(get_post(post_id))
    db.session.commit()
    return redirect(url_for('blog.index'))
