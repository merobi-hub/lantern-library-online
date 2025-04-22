from flask import Blueprint, render_template, request, redirect, url_for, flash
from book_inventory.models import User, db, Post, Book
from flask_login import login_required, current_user
from book_inventory.forms import BlogPostForm

lblog = Blueprint('lblog', __name__, template_folder='blog_templates')

@lblog.route('/blog', methods = ['GET', 'POST'])
@login_required
def blog():
    posts = Post.query.all()
    for post in posts:
        post.date_created = post.date_created.strftime('%a %d %b %Y, %I:%M%p')
    return render_template('blog.html', posts = posts)

@lblog.route('/createpost', methods = ['GET', 'POST'])
@login_required
def createpost():
    form = BlogPostForm()

    try:

        if request.method == 'POST' and form.validate_on_submit():
            post = form.content.data
            title = form.title.data
            email = current_user.email
            post = Post(title, post, email)
            db.session.add(post)
            db.session.commit()

            flash(f'Post created successfully.', 'user-created')

            return redirect(url_for('lblog.blog'))

    except:
        raise Exception("That didn't work. Please try again.")

    return render_template('createpost.html', form = form)