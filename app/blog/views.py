from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import blog
from .. import db
from ..models import Blog, User
from .forms import BlogPostForm


@blog.route('/tweet', methods=['GET', 'POST'])
@login_required
def tweet():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog = Blog(content=form.content.data, user=current_user.id)
        db.session.add(blog)
        db.session.commit()
        flash('You have successfully posted a tweet!')
        return redirect(url_for('blog.tweet'))
    tweets = Blog.query.filter_by(user=current_user.id)
    return render_template('blog/dashboard.html', form=form, tweets=tweets)


@blog.route('/follow/<int:followed_id>', methods=['GET', 'POST'])
@login_required
def follow(followed_id):
    user = User.query.get_or_404(followed_id)
    curr_user = current_user.follow(user)
    if curr_user:
        db.session.add(curr_user)
        db.session.commit()
        flash('You are now following {0}'.format(user.username))
    else:
        flash('You are already following {0}'.format(user.username))
    return redirect(url_for('blog.list_tweeters'))


@blog.route('/tweeters', methods=['GET', 'POST'])
@login_required
def list_tweeters():
    """
    List all users.
    """
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('blog/tweeters.html', tweeters=users)
