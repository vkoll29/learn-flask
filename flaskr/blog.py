from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        error = None

        if not title:
            error = 'Title is required'

        if error is None:
            db = get_db()
            db.execute(
                """INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)""",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        """
        SELECT p.id, title, body, created, author_id, username 
        FROM post p 
        JOIN user u on u.id = p.author_id
        """
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


def get_post(id, check_author=True):
    """
    Reusable function for getting posts. Need for updating and deleting posts.
    :param id: the id of the post to be retrieved
    :param check_author: check whether the author retrieving the post created it
    :return: post dictionary
    """
    post = get_db().execute(
        """
        SELECT p.id, title, body, created, author_id, username 
        FROM post p 
        JOIN user u on p.author_id = u.id
        WHERE p.id = ?
        """,
        (id, )
    ).fetchone()

    if post is None:
        abort(404, f"Post with id {id} does not exist")
    if check_author and post['author_id'] != g.user['id']:
        abort(403, "You're not allowed to make changes to this post")
    return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @load_logged_in_user
# def update(id):
#     post = get_post(id)
