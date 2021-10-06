from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from book_inventory.models import User, db, Book, Post
from book_inventory.forms import AddBookForm, UpdateBookForm, BlogPostForm

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/about')
def about():
    return render_template('about.html')

@site.route('/profile')
@login_required
def profile():
    """User profile containing book donations and blog posts."""
    user_donations = Book.query.filter_by(user_id=current_user.id).all()
    user_posts = Post.query.filter_by(email=current_user.email).all()
    return render_template('profile.html', user_donations = user_donations, user_posts = user_posts)

@site.route('/updatebook', methods = ['GET', 'POST'])
@login_required
def updatebook():
    """
    Returns pre-filled form for editing a catalog entry and processes inputs.
    """
    form = UpdateBookForm()
    id = request.args.get('id', None)
    title = request.args.get('title', None)
    author = request.args.get('author', None)
    publisher = request.args.get('publisher', None)
    description = request.args.get('description', None)
    genre = request.args.get('genre', None)
    pub_date = request.args.get('pub_date', None)
    print(id)
    print(publisher)
    try:
        if request.method == 'POST' and form.validate_on_submit():
            Book.query.filter_by(id=id).update({
                "author": (form.author.data),
                "title": (form.title.data),
                "publisher": (form.publisher.data),
                "description": (form.description.data),
                "genre": (form.genre.data),
                "pub_date": (form.pub_date.data),
                "user_id": (current_user.id)
            })
            db.session.commit()

            flash(f'Thank you! The record for {form.title.data} has been updated.', 'user-created')

            return redirect(url_for('catalog.books'))
    except:
        raise Exception("That didn't work. Please try again.")
    
    return render_template(
        'updatebook.html', 
        form=form, 
        title=title, 
        author=author,
        publisher=publisher,
        description=description,
        genre=genre,
        pub_date=pub_date
        )

@site.route('/updatepost', methods = ['GET', 'POST'])
@login_required
def updateblog():
    """
    Returns pre-filled form for editing a blog post and processes inputs.
    """
    form = BlogPostForm()
    id = request.args.get('id', None)
    old_content = request.args.get('content', None)
    old_title = request.args.get('title', None)

    try:
        if request.method == 'POST' and form.validate_on_submit():
            Post.query.filter_by(id=id).update({
                "title": (form.title.data),
                "content": (form.content.data),
                "email": (current_user.email)
            })
            db.session.commit()

            flash(f'The post has been updated.', 'user-created')

            return redirect(url_for('lblog.blog'))
    except:
        raise Exception("That didn't work. Please try again.")

    return render_template(
        'updatepost.html', 
        form=form, 
        old_content=old_content, 
        old_title=old_title
        )

@site.route('/deletepost', methods = ['GET', 'POST'])
@login_required
def deletepost():
    """Deletes a blog post."""
    id = request.args.get('id', None)
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'The post has been deleted.', 'user-created')
    return redirect(url_for('site.profile'))