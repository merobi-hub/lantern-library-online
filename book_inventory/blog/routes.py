from flask import Blueprint, render_template, request, redirect, url_for
from book_inventory.models import User, db, Post, Book
from flask_login import login_required, current_user
from book_inventory.forms import BlogPostForm

lblog = Blueprint('lblog', __name__, template_folder='blog_templates')

@lblog.route('/blog', methods = ['GET', 'POST'])
@login_required
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts = posts)

@lblog.route('/createpost', methods = ['GET', 'POST'])
@login_required
def createpost():
    form = BlogPostForm()
    if request.method == 'POST' and form.validate():
        post = form.content.data
        title = form.title.data
        email = current_user.email
        post = Post(title, post, email)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('lblog.blog'))
    return render_template('createpost.html', form = form)